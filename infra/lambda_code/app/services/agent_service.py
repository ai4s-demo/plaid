"""AI Agent service using Amazon Bedrock."""
import json
import re
from typing import AsyncGenerator, Dict, List, Optional
import boto3

from app.config import settings
from app.models import DesignParameters, PlateType, Distribution, GeneConfig
from app.solver.constraints import CONSTRAINT_EXPLANATIONS


class AgentService:
    """AI Agent service for natural language interaction."""
    
    SYSTEM_PROMPT = """你是 Smart Campaign Designer 的 AI 助手，帮助科学家设计微孔板布局。

你的能力:
1. 理解中英文自然语言描述的实验需求
2. 提取设计参数（基因数、重复数、板类型、分布方式等）
3. 当信息不完整时，主动询问缺失信息
4. 解释 PLAID 约束和设计原理
5. 提供优化建议

当用户描述需求时，提取以下参数:
- plate_type: 板类型 (96/384/1536)，默认 96
- replicates: 每个基因的重复数，默认 6
- edge_empty_layers: 边缘空白层数，默认 1
- distribution: 分布方式 (random/column/row/uniform)，默认 uniform
- transfer_volume: 转移体积 (nL)，默认 2500 (2.5ul)
- gene_configs: 每个基因的特定配置（如果不同基因有不同重复数）

如果用户没有提供某个参数，使用默认值但要告知用户。
如果用户的需求不清楚，主动询问澄清。

回复时使用用户的语言（中文或英文）。"""

    PARAM_EXTRACTION_PROMPT = """你是一个参数提取助手。根据用户的实验设计需求，提取结构化参数。

请分析用户的需求，输出一个 JSON 对象，包含以下字段：
{
  "plate_type": 96 | 384 | 1536,
  "default_replicates": 数字（默认重复数）,
  "edge_empty_layers": 数字（边缘空白层数，"最外面两圈"=2）,
  "distribution": "random" | "uniform" | "column" | "row",
  "transfer_volume_nl": 数字（转移体积，单位nL，2ul=2000nL）,
  "gene_selection": {
    "type": "first_n" | "specific" | "all",
    "count": 数字（如果是first_n）,
    "genes": ["基因名列表"]（如果是specific），
    "additional_genes": ["额外基因名列表"]（如果需要在first_n基础上添加特定基因）
  },
  "gene_configs": {
    "基因名": {"replicates": 数字, "transfer_volume_nl": 数字}
  }
}

重要规则：
1. 如果用户说"前N个基因"加上"GeneX要M次重复"，需要：
   - gene_selection.type = "first_n", count = N
   - gene_selection.additional_genes = ["GeneX"]（如果GeneX不在前N个中）
   - gene_configs["GeneX"] = {"replicates": M}

2. 基因名格式通常是 "Gene1", "Gene2", ..., "Gene25" 等

示例1：
用户："384板，前9个基因每个8个重复，第10个基因20个重复，边缘2层，转移2ul"
输出：
{
  "plate_type": 384,
  "default_replicates": 8,
  "edge_empty_layers": 2,
  "distribution": "uniform",
  "transfer_volume_nl": 2000,
  "gene_selection": {"type": "first_n", "count": 10},
  "gene_configs": {
    "Gene10": {"replicates": 20}
  }
}

示例2：
用户："前10个基因，8个重复，Gene25要120次重复，用1536的板子"
输出：
{
  "plate_type": 1536,
  "default_replicates": 8,
  "edge_empty_layers": 1,
  "distribution": "uniform",
  "transfer_volume_nl": 2500,
  "gene_selection": {"type": "first_n", "count": 10, "additional_genes": ["Gene25"]},
  "gene_configs": {
    "Gene25": {"replicates": 120}
  }
}

示例3：
用户："96孔板，6个重复，随机分布"
输出：
{
  "plate_type": 96,
  "default_replicates": 6,
  "edge_empty_layers": 1,
  "distribution": "random",
  "transfer_volume_nl": 2500,
  "gene_selection": {"type": "all"},
  "gene_configs": {}
}

只输出 JSON，不要其他文字。"""

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
        """Use AI to extract structured parameters from natural language."""
        
        if not self.client:
            return None
        
        prompt = f"""用户需求: {message}

可用的基因列表（按自然排序）: {', '.join(available_genes[:20])}{'...' if len(available_genes) > 20 else ''}
总共 {len(available_genes)} 个基因。

请提取参数并输出 JSON。"""

        try:
            response = self.client.invoke_model(
                modelId=settings.bedrock_model_id,
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 1024,
                    "system": self.PARAM_EXTRACTION_PROMPT,
                    "messages": [{"role": "user", "content": prompt}]
                })
            )
            
            result = json.loads(response['body'].read())
            content = result.get('content', [{}])[0].get('text', '{}')
            
            # 提取 JSON（可能被包裹在 ```json ``` 中）
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                params = json.loads(json_match.group())
                print(f"[AI] 提取的参数: {json.dumps(params, ensure_ascii=False, indent=2)}")
                return params
            
        except Exception as e:
            print(f"[AI] 参数提取失败: {e}")
        
        return None
    
    def build_params_from_ai_result(
        self,
        ai_params: Dict,
        available_genes: List[str]
    ) -> tuple:
        """Convert AI extracted params to DesignParameters and gene list."""
        
        params = DesignParameters.default()
        
        # 板类型
        plate_type = ai_params.get('plate_type', 96)
        if plate_type == 384:
            params.plate_type = PlateType.PLATE_384
        elif plate_type == 1536:
            params.plate_type = PlateType.PLATE_1536
        else:
            params.plate_type = PlateType.PLATE_96
        
        # 默认重复数
        params.replicates = ai_params.get('default_replicates', 6)
        
        # 边缘层数
        params.edge_empty_layers = ai_params.get('edge_empty_layers', 1)
        
        # 分布方式
        dist = ai_params.get('distribution', 'uniform')
        params.distribution = Distribution(dist) if dist in ['random', 'uniform', 'column', 'row'] else Distribution.UNIFORM
        
        # 转移体积
        params.transfer_volume = ai_params.get('transfer_volume_nl', 2500)
        
        # 基因选择
        gene_selection = ai_params.get('gene_selection', {'type': 'all'})
        selected_genes = available_genes
        
        if gene_selection.get('type') == 'first_n':
            count = gene_selection.get('count', len(available_genes))
            selected_genes = available_genes[:count]
            
            # 处理额外基因（不在前N个中但需要特殊配置的）
            additional_genes = gene_selection.get('additional_genes', [])
            for gene in additional_genes:
                if gene in available_genes and gene not in selected_genes:
                    selected_genes.append(gene)
                    
        elif gene_selection.get('type') == 'specific':
            specific = gene_selection.get('genes', [])
            selected_genes = [g for g in available_genes if g in specific]
        
        # 每个基因的特定配置
        gene_configs = ai_params.get('gene_configs', {})
        for gene_key, config in gene_configs.items():
            # 支持 "Gene10" 或 "Gene1-Gene9" 格式
            if '-' in gene_key:
                # 范围格式 - 暂不处理
                pass
            else:
                # 单个基因 - 确保该基因在选中列表中
                if gene_key in available_genes:
                    # 如果基因不在选中列表中，添加它
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
        """
        Chat with the AI agent.
        
        Args:
            message: User message
            history: Conversation history
            context: Additional context (source_data, layout, etc.)
            
        Yields:
            Response chunks
        """
        # If Bedrock is not available, use mock response
        if not self.client:
            yield "你好！我是 Smart Campaign Designer 的 AI 助手。"
            yield "\n\n"
            yield "目前 AWS Bedrock 服务未配置，但你仍然可以："
            yield "\n- 上传源板文件（Excel/CSV）"
            yield "\n- 生成板布局"
            yield "\n- 拖拽调整布局"
            yield "\n- 导出 Picklist"
            yield "\n\n"
            yield "请先上传你的源板文件开始设计！"
            return
        
        # Build messages
        messages = self._build_messages(message, history, context)
        
        try:
            # Call Bedrock
            response = self.client.invoke_model_with_response_stream(
                modelId=settings.bedrock_model_id,
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 2048,
                    "system": self.SYSTEM_PROMPT,
                    "messages": messages
                })
            )
            
            # Stream response
            for event in response['body']:
                chunk = json.loads(event['chunk']['bytes'])
                if chunk['type'] == 'content_block_delta':
                    text = chunk['delta'].get('text', '')
                    if text:
                        yield text
                    
        except Exception as e:
            yield f"AI 服务错误: {str(e)}"
    
    def _build_messages(
        self,
        message: str,
        history: List[Dict],
        context: Optional[Dict]
    ) -> List[Dict]:
        """Build messages for Bedrock API."""
        messages = []
        
        # Add history with role alternation fix
        last_role = None
        for h in history[-10:]:  # Keep last 10 messages
            role = h.get("role", "user")
            content = h.get("content", "")
            if not content:
                continue
                
            # If same role as last, merge content
            if role == last_role and messages:
                messages[-1]["content"] += "\n\n" + content
            else:
                messages.append({
                    "role": role,
                    "content": content
                })
                last_role = role
        
        # Add context to current message
        content = message
        if context:
            if context.get("sourcePlate"):
                genes = context["sourcePlate"].get("wells", [])
                gene_names = [w.get("geneName", w.get("geneId", "")) for w in genes[:5]]
                content += f"\n\n[上下文: 已上传源板，包含 {len(genes)} 个基因: {', '.join(gene_names)}{'...' if len(genes) > 5 else ''}]"
            if context.get("currentLayout"):
                content += "\n\n[上下文: 已生成布局]"
        
        # Handle the new user message
        if last_role == "user" and messages:
            # Merge with last user message
            messages[-1]["content"] += "\n\n" + content
        else:
            messages.append({
                "role": "user",
                "content": content
            })
        
        # Ensure messages start with user (Claude requirement)
        if messages and messages[0]["role"] != "user":
            messages = messages[1:]
        
        # Ensure we have at least one message
        if not messages:
            messages = [{"role": "user", "content": message}]
        
        return messages
    
    def extract_parameters(
        self,
        message: str,
        history: List[Dict] = None,
        num_genes: int = None,
    ) -> DesignParameters:
        """
        Extract design parameters from natural language.
        
        Args:
            message: User message
            history: Conversation history
            num_genes: Number of genes (for auto plate type selection)
            
        Returns:
            Extracted DesignParameters
        """
        params = DesignParameters.default()
        
        # Combine message with recent history
        text = message.lower()
        if history:
            for h in history[-3:]:
                text += " " + h.get("content", "").lower()
        
        # Extract plate type (user explicit choice)
        user_specified_plate = False
        if "1536" in text:
            params.plate_type = PlateType.PLATE_1536
            user_specified_plate = True
        elif "384" in text:
            params.plate_type = PlateType.PLATE_384
            user_specified_plate = True
        elif "96" in text:
            params.plate_type = PlateType.PLATE_96
            user_specified_plate = True
        
        # Extract replicates
        rep_patterns = [
            r'(\d+)\s*(?:个)?(?:重复|replicate|rep)',
            r'(?:重复|replicate|rep)\s*(?:数)?[：:]\s*(\d+)',
            r'each\s+(?:gene\s+)?(\d+)\s+(?:times|replicates)',
        ]
        for pattern in rep_patterns:
            match = re.search(pattern, text)
            if match:
                params.replicates = int(match.group(1))
                break
        
        # Extract edge empty
        edge_patterns = [
            r'(?:边缘|外圈|edge)\s*(?:空白|留空|empty)?\s*(\d+)\s*(?:层|layer)?',
            r'(\d+)\s*(?:层|layer)\s*(?:边缘|外圈|edge)',
            r'leave\s+(\d+)\s+(?:outer\s+)?layer',
        ]
        for pattern in edge_patterns:
            match = re.search(pattern, text)
            if match:
                params.edge_empty_layers = int(match.group(1))
                break
        
        # Check for "外圈留空" without number
        if "外圈留空" in text or "边缘留空" in text or "leave outer" in text:
            if params.edge_empty_layers == 0:
                params.edge_empty_layers = 1
        
        # Extract distribution
        if "随机" in text or "random" in text:
            params.distribution = Distribution.RANDOM
        elif "按列" in text or "column" in text:
            params.distribution = Distribution.COLUMN
        elif "按行" in text or "row" in text:
            params.distribution = Distribution.ROW
        elif "均匀" in text or "uniform" in text:
            params.distribution = Distribution.UNIFORM
        
        # Extract transfer volume
        volume_patterns = [
            r'(?:转移|transfer)\s*(\d+(?:\.\d+)?)\s*(?:ul|μl|微升)',
            r'(\d+(?:\.\d+)?)\s*(?:ul|μl|微升)\s*(?:转移|transfer)?',
            r'(?:volume|体积)[：:]\s*(\d+(?:\.\d+)?)',
        ]
        for pattern in volume_patterns:
            match = re.search(pattern, text)
            if match:
                volume = float(match.group(1))
                # 如果是 ul，转换为 nL (1 ul = 1000 nL)
                if 'ul' in text or 'μl' in text or '微升' in text:
                    params.transfer_volume = volume * 1000  # 转换为 nL
                else:
                    params.transfer_volume = volume
                break
        
        # Auto-select plate type if not specified and we know gene count
        if not user_specified_plate and num_genes is not None:
            total_samples = num_genes * params.replicates
            edge = params.edge_empty_layers
            
            # Calculate available wells for each plate type
            # 96-well: 8x12, inner = (8-2*edge) * (12-2*edge)
            # 384-well: 16x24, inner = (16-2*edge) * (24-2*edge)
            # 1536-well: 32x48, inner = (32-2*edge) * (48-2*edge)
            
            wells_96 = (8 - 2*edge) * (12 - 2*edge) if edge < 4 else 0
            wells_384 = (16 - 2*edge) * (24 - 2*edge) if edge < 8 else 0
            wells_1536 = (32 - 2*edge) * (48 - 2*edge) if edge < 16 else 0
            
            if total_samples <= wells_96:
                params.plate_type = PlateType.PLATE_96
            elif total_samples <= wells_384:
                params.plate_type = PlateType.PLATE_384
            elif total_samples <= wells_1536:
                params.plate_type = PlateType.PLATE_1536
            # else: keep default 96 and let solver handle multi-plate
        
        return params
    
    def extract_gene_count(self, message: str, total_genes: int) -> Optional[int]:
        """
        Extract gene count from natural language.
        
        Args:
            message: User message
            total_genes: Total available genes
            
        Returns:
            Number of genes to use, or None to use all
        """
        text = message.lower()
        
        # Patterns for gene count
        patterns = [
            r'前\s*(\d+)\s*个\s*(?:基因|gene)?',  # 前10个基因
            r'(?:前|first)\s*(\d+)',  # 前10 / first 10
            r'(\d+)\s*个\s*(?:基因|gene)',  # 10个基因
            r'(\d+)\s*genes?',  # 10 genes
            r'(?:用|use|选|select)\s*(\d+)',  # 用10个 / use 10
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                count = int(match.group(1))
                # Ensure count is within bounds
                return min(count, total_genes)
        
        return None  # Use all genes
    
    def detect_intent(self, message: str) -> str:
        """
        Detect user intent from message.
        
        Args:
            message: User message
            
        Returns:
            Intent string
        """
        text = message.lower()
        
        # Intent keywords
        intents = {
            'UPLOAD_FILE': ['上传', 'upload', '文件', 'file', 'excel', 'csv'],
            'DESIGN_PLATE': ['设计', 'design', '布局', 'layout', '基因', 'gene', 
                           '重复', 'replicate', '孔板', 'plate'],
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
            f"未知约束: {constraint_name}"
        )
    
    def generate_missing_params_question(
        self,
        params: DesignParameters,
        source_genes: List[str] = None
    ) -> Optional[str]:
        """
        Generate question for missing parameters.
        
        Args:
            params: Current parameters
            source_genes: Genes from source plate
            
        Returns:
            Question string or None if all params are set
        """
        questions = []
        
        # Check if we have source data
        if not source_genes:
            return "请先上传源板文件（Excel 或 CSV 格式），我需要知道您要处理哪些基因。"
        
        # All required params have defaults, so just confirm
        return None
