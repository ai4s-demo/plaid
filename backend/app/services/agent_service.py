"""AI Agent service using Amazon Bedrock with structured tool_use output."""
import json
import re
from typing import AsyncGenerator, Dict, List, Optional
import boto3

from app.config import settings
from app.models import DesignParameters, PlateType, Distribution, GeneConfig
from app.solver.constraints import CONSTRAINT_EXPLANATIONS

# Tool schema for structured parameter extraction
EXTRACT_PARAMS_TOOL = {
    "name": "extract_design_params",
    "description": "Extract plate design parameters from the user's request.",
    "input_schema": {
        "type": "object",
        "properties": {
            "plate_type": {
                "type": "integer",
                "enum": [96, 384, 1536],
                "description": "Plate type (well count). Default 96."
            },
            "default_replicates": {
                "type": "integer",
                "description": "Default number of replicates per gene. Default 6."
            },
            "edge_empty_layers": {
                "type": "integer",
                "description": "Number of empty edge layers around the plate border. '2 edge layers empty' or '外围两层留空' = 2. Default 1."
            },
            "distribution": {
                "type": "string",
                "enum": ["random", "uniform", "column", "row"],
                "description": "Sample distribution strategy. Default 'uniform'."
            },
            "transfer_volume_nl": {
                "type": "number",
                "description": "Transfer volume in nL. 2ul = 2000nL, 2.5ul = 2500nL. Default 2500."
            },
            "gene_selection": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "enum": ["first_n", "specific", "all"],
                        "description": "'first_n': use first N genes; 'specific': use named genes; 'all': use all."
                    },
                    "count": {
                        "type": "integer",
                        "description": "Number of genes if type is 'first_n'."
                    },
                    "genes": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Gene names if type is 'specific'."
                    },
                    "additional_genes": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Extra genes to add beyond the first_n selection."
                    }
                },
                "required": ["type"]
            },
            "gene_configs": {
                "type": "object",
                "description": "Per-gene overrides. Keys are gene names, values have 'replicates' and/or 'transfer_volume_nl'.",
                "additionalProperties": {
                    "type": "object",
                    "properties": {
                        "replicates": {"type": "integer"},
                        "transfer_volume_nl": {"type": "number"}
                    }
                }
            }
        },
        "required": ["plate_type", "default_replicates", "edge_empty_layers", "gene_selection"]
    }
}


class AgentService:
    """AI Agent service for natural language interaction."""

    SYSTEM_PROMPT = """You are the AI assistant for Smart Campaign Designer, helping scientists design microplate layouts.

Your capabilities:
1. Understand experiment requirements described in Chinese or English
2. Extract design parameters (gene count, replicates, plate type, distribution, etc.)
3. Ask for missing information when the request is incomplete
4. Explain PLAID constraints and design principles
5. Provide optimization suggestions

Reply in the same language the user uses (Chinese or English)."""

    PARAM_EXTRACTION_SYSTEM = """You are a parameter extraction assistant for a microplate layout design tool.
Analyze the user's experiment design request and call the extract_design_params tool with the correct parameters.

Rules:
- Gene names are typically "Gene1", "Gene2", ..., "Gene25", etc.
- "前N个基因" / "first N genes" → gene_selection.type = "first_n", count = N
- "外围两层留空" / "2 edge layers empty" → edge_empty_layers = 2
- "2ul" / "2微升" → transfer_volume_nl = 2000
- If a parameter is not mentioned, use sensible defaults (plate_type=96, replicates=6, edge=1, distribution=uniform, volume=2500)
- If a specific gene needs different replicates, put it in gene_configs AND ensure it's selected"""

    def __init__(self):
        self.client = None
        self._init_client()

    def _init_client(self):
        """Initialize Bedrock client."""
        try:
            self.client = boto3.client(
                'bedrock-runtime',
                region_name=settings.aws_region
            )
        except Exception as e:
            print(f"Warning: Could not initialize Bedrock client: {e}")
            self.client = None

    async def extract_params_with_ai(
        self,
        message: str,
        available_genes: List[str]
    ) -> Dict:
        """Use AI tool_use to extract structured parameters from natural language."""

        if not self.client:
            return None

        gene_list = ', '.join(available_genes[:20])
        gene_suffix = '...' if len(available_genes) > 20 else ''
        prompt = f"""User request: {message}

Available genes (natural sort): {gene_list}{gene_suffix}
Total: {len(available_genes)} genes.

Extract the design parameters and call the tool."""

        try:
            response = self.client.invoke_model(
                modelId=settings.bedrock_model_id,
                body=json.dumps({
                    "dsf": "bedrock-2023-05-31",
                    "max_tokens": 1024,
                    "system": self.PARAM_EXTRACTION_SYSTEM,
                    "tools": [EXTRACT_PARAMS_TOOL],
                    "tool_choice": {"type": "tool", "name": "extract_design_params"},
                    "messages": [{"role": "user", "content": prompt}]
                })
            )

            result = json.loads(response['body'].read())

            # Extract tool_use input from response
            for block in result.get('content', []):
                if block.get('type') == 'tool_use' and block.get('name') == 'extract_design_params':
                    params = block['input']
                    print(f"[AI] Extracted params: {json.dumps(params, ensure_ascii=False, indent=2)}")
                    return params

        except Exception as e:
            print(f"[AI] Parameter extraction failed: {e}")

        return None

    def build_params_from_ai_result(
        self,
        ai_params: Dict,
        available_genes: List[str],
        user_message: str = "",
    ) -> tuple:
        """Convert AI extracted params to DesignParameters and gene list."""

        params = DesignParameters.default()

        plate_type = ai_params.get('plate_type', 96)
        if plate_type == 384:
            params.plate_type = PlateType.PLATE_384
        elif plate_type == 1536:
            params.plate_type = PlateType.PLATE_1536
        else:
            params.plate_type = PlateType.PLATE_96

        params.replicates = ai_params.get('default_replicates', 6)
        params.edge_empty_layers = ai_params.get('edge_empty_layers', 1)

        dist = ai_params.get('distribution', 'uniform')
        params.distribution = Distribution(dist) if dist in ['random', 'uniform', 'column', 'row'] else Distribution.UNIFORM

        params.transfer_volume = ai_params.get('transfer_volume_nl', 2500)

        # Gene selection
        gene_selection = ai_params.get('gene_selection', {'type': 'all'})
        selected_genes = available_genes

        if gene_selection.get('type') == 'first_n':
            count = gene_selection.get('count', len(available_genes))
            selected_genes = available_genes[:count]

            for gene in gene_selection.get('additional_genes', []):
                if gene in available_genes and gene not in selected_genes:
                    selected_genes.append(gene)

        elif gene_selection.get('type') == 'specific':
            specific = gene_selection.get('genes', [])
            selected_genes = [g for g in available_genes if g in specific]

        # Per-gene configs
        for gene_key, config in ai_params.get('gene_configs', {}).items():
            if gene_key in available_genes:
                if gene_key not in selected_genes:
                    selected_genes.append(gene_key)

                params.gene_configs[gene_key] = GeneConfig(
                    gene_symbol=gene_key,
                    replicates=config.get('replicates', params.replicates),
                    transfer_volume=config.get('transfer_volume_nl', params.transfer_volume)
                )

        return params, selected_genes

    async def chat(
        self,
        message: str,
        history: List[Dict],
        context: Optional[Dict] = None
    ) -> AsyncGenerator[str, None]:
        """Stream chat response from Bedrock."""
        if not self.client:
            yield "Hello! I'm the Smart Campaign Designer AI assistant."
            yield "\n\nAWS Bedrock is not configured, but you can still:"
            yield "\n- Upload source plate files (Excel/CSV)"
            yield "\n- Generate plate layouts"
            yield "\n- Drag and drop to adjust layouts"
            yield "\n- Export Picklist"
            yield "\n\nPlease upload your source plate file to get started!"
            return

        messages = self._build_messages(message, history, context)

        try:
            response = self.client.invoke_model_with_response_stream(
                modelId=settings.bedrock_model_id,
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 2048,
                    "system": self.SYSTEM_PROMPT,
                    "messages": messages
                })
            )

            for event in response['body']:
                chunk = json.loads(event['chunk']['bytes'])
                if chunk['type'] == 'content_block_delta':
                    text = chunk['delta'].get('text', '')
                    if text:
                        yield text

        except Exception as e:
            yield f"AI service error: {str(e)}"

    def _build_messages(
        self,
        message: str,
        history: List[Dict],
        context: Optional[Dict]
    ) -> List[Dict]:
        """Build messages for Bedrock API."""
        messages = []

        last_role = None
        for h in history[-10:]:
            role = h.get("role", "user")
            content = h.get("content", "")
            if not content:
                continue

            if role == last_role and messages:
                messages[-1]["content"] += "\n\n" + content
            else:
                messages.append({"role": role, "content": content})
                last_role = role

        content = message
        if context:
            if context.get("sourcePlate"):
                genes = context["sourcePlate"].get("wells", [])
                gene_names = [w.get("geneName", w.get("geneId", "")) for w in genes[:5]]
                suffix = '...' if len(genes) > 5 else ''
                content += f"\n\n[Context: Source plate uploaded with {len(genes)} genes: {', '.join(gene_names)}{suffix}]"
            if context.get("currentLayout"):
                content += "\n\n[Context: Layout already generated]"

        if last_role == "user" and messages:
            messages[-1]["content"] += "\n\n" + content
        else:
            messages.append({"role": "user", "content": content})

        if messages and messages[0]["role"] != "user":
            messages = messages[1:]

        if not messages:
            messages = [{"role": "user", "content": message}]

        return messages

    def detect_intent(self, message: str) -> str:
        """Detect user intent from message."""
        text = message.lower()

        intents = {
            'UPLOAD_FILE': ['上传', 'upload', '文件', 'file', 'excel', 'csv'],
            'DESIGN_PLATE': ['设计', 'design', '布局', 'layout', '基因', 'gene',
                           '重复', 'replicate', '孔板', 'plate', 'well'],
            'MODIFY_LAYOUT': ['修改', 'modify', '调整', 'adjust', '移动', 'move',
                            '交换', 'swap', '拖拽', 'drag'],
            'GENERATE_PICKLIST': ['生成', 'generate', 'picklist', '清单',
                                 '导出', 'export', '下载', 'download'],
            'EXPLAIN': ['解释', 'explain', '为什么', 'why', '约束', 'constraint',
                       '什么是', 'what is', '原理', 'principle'],
            'VALIDATE': ['验证', 'validate', '检查', 'check', '是否满足', 'satisfy'],
        }

        for intent, keywords in intents.items():
            if any(kw in text for kw in keywords):
                return intent

        return 'GENERAL'

    def get_constraint_explanation(self, constraint_name: str) -> str:
        """Get explanation for a constraint."""
        return CONSTRAINT_EXPLANATIONS.get(
            constraint_name,
            f"Unknown constraint: {constraint_name}"
        )
