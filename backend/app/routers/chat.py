"""Chat API with SSE streaming."""
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor

from app.services import AgentService, LayoutService
from app.models import DesignParameters, SourcePlate, SourceWell, SolveStatus

router = APIRouter()

# Lazy initialization to avoid Bedrock client creation at import time
_agent_service = None
_layout_service = None

def get_agent_service():
    global _agent_service
    if _agent_service is None:
        _agent_service = AgentService()
    return _agent_service

def get_layout_service():
    global _layout_service
    if _layout_service is None:
        _layout_service = LayoutService()
    return _layout_service


class ChatRequest(BaseModel):
    """Chat request model."""
    message: str
    history: List[Dict] = []
    context: Optional[Dict] = None


class ExtractRequest(BaseModel):
    """Parameter extraction request."""
    message: str
    history: List[Dict] = []


@router.post("/")
async def chat(request: ChatRequest):
    """
    Chat with AI agent using SSE streaming.
    """
    async def generate():
        agent_service = get_agent_service()
        layout_service = get_layout_service()
        try:
            # 检测意图
            intent = agent_service.detect_intent(request.message)
            
            # 如果是设计布局意图且有源板数据，自动生成布局
            if intent == 'DESIGN_PLATE' and request.context and request.context.get('sourcePlate'):
                # 发送开始消息
                yield f"data: {json.dumps({'type': 'text', 'content': '正在分析您的需求...'}, ensure_ascii=False)}\n\n"
                await asyncio.sleep(0)
                
                try:
                    # 转换源板数据
                    source_data = request.context['sourcePlate']
                    wells_data = []
                    for w in source_data.get('wells', []):
                        # 前端字段名可能是 wellId/geneId 或 position/gene_symbol
                        position = w.get('wellId') or w.get('position', '')
                        gene = w.get('geneId') or w.get('gene_symbol', '')
                        volume = w.get('volume', 100)
                        if position and gene:
                            wells_data.append(SourceWell(
                                position=position,
                                gene_symbol=gene,
                                volume=volume
                            ))
                    
                    # 获取所有唯一基因并使用自然排序 (Gene1, Gene2, ..., Gene10, Gene11)
                    import re
                    def natural_sort_key(s):
                        return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', s)]
                    
                    all_genes = sorted(list(set(w.gene_symbol for w in wells_data)), key=natural_sort_key)
                    
                    # Extract structured parameters via LLM tool_use
                    ai_params = await agent_service.extract_params_with_ai(request.message, all_genes)

                    if ai_params:
                        params, selected_genes = agent_service.build_params_from_ai_result(ai_params, all_genes)
                        wells_data = [w for w in wells_data if w.gene_symbol in selected_genes]
                    else:
                        # Fallback: use all genes with defaults
                        selected_genes = all_genes
                        params = DesignParameters.default()

                    gene_info = f"Selected {len(selected_genes)} genes"

                    yield f"data: {json.dumps({'type': 'text', 'content': 'Parameters parsed, generating layout...'})}\n\n"
                    await asyncio.sleep(0)
                    
                    source_plate = SourcePlate(
                        barcode=source_data.get('plateId') or source_data.get('barcode', 'SOURCE_PLATE'),
                        wells=wells_data
                    )
                    
                    print(f"[DEBUG] Source plate: {source_plate.barcode}, wells: {len(source_plate.wells)}, genes: {len(source_plate.get_genes())}, plate_type: {params.plate_type}")
                    print(f"[DEBUG] Gene configs: {params.gene_configs}")
                    
                    # 生成布局（在后台线程运行，主协程发送心跳保活 SSE）
                    loop = asyncio.get_event_loop()
                    executor = ThreadPoolExecutor(max_workers=1)
                    future = loop.run_in_executor(
                        executor,
                        layout_service.generate_layout,
                        source_plate,
                        params,
                    )

                    while not future.done():
                        yield f"data: {json.dumps({'type': 'heartbeat'})}\n\n"
                        try:
                            await asyncio.wait_for(asyncio.shield(future), timeout=10)
                        except asyncio.TimeoutError:
                            pass

                    result = await future

                    if result.status == SolveStatus.SUCCESS or result.status == SolveStatus.PARTIAL:
                        layouts = result.layouts or []
                        if layouts:
                            # Convert all plates to frontend format
                            frontend_layouts = []
                            for layout in layouts:
                                frontend_layout = {
                                    'layoutId': f'layout_{layout.plate_index}',
                                    'plateFormat': layout.plate_type.value,
                                    'plateIndex': layout.plate_index,
                                    'plateBarcode': layout.plate_barcode,
                                    'wells': [
                                        {
                                            'wellId': w.position,
                                            'row': w.row,
                                            'col': w.col,
                                            'geneId': w.gene_symbol,
                                            'geneName': w.gene_symbol,
                                            'wellType': w.content_type.value,
                                            'replicateIndex': w.replicate_index or 0
                                        }
                                        for w in layout.wells
                                    ],
                                    'violations': [
                                        {
                                            'type': v.constraint_name,
                                            'severity': v.severity,
                                            'message': v.description,
                                            'wells': v.affected_wells
                                        }
                                        for v in (result.violations or [])
                                    ],
                                    'score': 1.0 - len(result.violations or []) * 0.1,
                                    'createdAt': ''
                                }
                                frontend_layouts.append(frontend_layout)

                            # Send first layout for backward compatibility
                            yield f"data: {json.dumps({'type': 'layout', 'content': frontend_layouts[0]}, ensure_ascii=False)}\n\n"
                            await asyncio.sleep(0)

                            # Send all layouts if multiple plates
                            if len(frontend_layouts) > 1:
                                yield f"data: {json.dumps({'type': 'layouts', 'content': frontend_layouts}, ensure_ascii=False)}\n\n"
                                await asyncio.sleep(0)

                            plate_info = f"{params.plate_type.value}孔板"

                            total_samples = sum(params.get_replicates_for_gene(g) for g in selected_genes)

                            if params.gene_configs:
                                special_configs = [f"{g}({c.replicates}x)" for g, c in params.gene_configs.items()]
                                config_detail = f", special: {', '.join(special_configs)}"
                            else:
                                config_detail = ""

                            num_plates = len(frontend_layouts)
                            plate_count_info = f", {num_plates} plates" if num_plates > 1 else ""
                            msg = f'\n\nLayout generated! {gene_info}, {params.replicates} replicates each{config_detail}, {total_samples} total samples, {plate_info}{plate_count_info}.'
                            yield f"data: {json.dumps({'type': 'text', 'content': msg})}\n\n"
                        else:
                            yield f"data: {json.dumps({'type': 'text', 'content': 'Layout generation failed. Please check parameters.'})}\n\n"
                    else:
                        msg = f'\n\n{result.message}'
                        yield f"data: {json.dumps({'type': 'text', 'content': msg})}\n\n"
                        
                except Exception as e:
                    msg = f'\n\n布局生成错误: {str(e)}'
                    yield f"data: {json.dumps({'type': 'text', 'content': msg}, ensure_ascii=False)}\n\n"
            else:
                # 普通对话
                async for chunk in agent_service.chat(
                    message=request.message,
                    history=request.history,
                    context=request.context
                ):
                    data = json.dumps({'type': 'text', 'content': chunk}, ensure_ascii=False)
                    yield f"data: {data}\n\n"
                    await asyncio.sleep(0)
                
                # 如果没有源板但想生成布局，提示上传
                if intent == 'DESIGN_PLATE' and (not request.context or not request.context.get('sourcePlate')):
                    msg = '\n\n💡 提示：请先上传源板文件（Excel/CSV），我才能为您生成布局。'
                    yield f"data: {json.dumps({'type': 'text', 'content': msg}, ensure_ascii=False)}\n\n"
            
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
        except Exception as e:
            error_data = json.dumps({'type': 'error', 'content': str(e)}, ensure_ascii=False)
            yield f"data: {error_data}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )


@router.post("/extract-parameters", response_model=DesignParameters)
async def extract_parameters(request: ExtractRequest):
    """
    Extract design parameters from natural language.
    """
    agent_service = get_agent_service()
    params = agent_service.extract_parameters(
        message=request.message,
        history=request.history
    )
    return params


@router.post("/detect-intent")
async def detect_intent(request: ExtractRequest):
    """
    Detect user intent from message.
    """
    agent_service = get_agent_service()
    intent = agent_service.detect_intent(request.message)
    return {"intent": intent}


@router.get("/explain/{constraint_name}")
async def explain_constraint(constraint_name: str):
    """
    Get explanation for a constraint.
    """
    agent_service = get_agent_service()
    explanation = agent_service.get_constraint_explanation(constraint_name)
    return {"constraint": constraint_name, "explanation": explanation}
