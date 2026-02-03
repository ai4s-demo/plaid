"""Chat API with SSE streaming."""
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
import json
import asyncio

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
                    
                    # 尝试使用 AI 提取结构化参数
                    ai_params = await agent_service.extract_params_with_ai(request.message, all_genes)
                    
                    if ai_params:
                        # 使用 AI 提取的参数
                        params, selected_genes = agent_service.build_params_from_ai_result(ai_params, all_genes)
                        wells_data = [w for w in wells_data if w.gene_symbol in selected_genes]
                        
                        # 构建基因信息
                        gene_configs_info = ""
                        if params.gene_configs:
                            configs = [f"{g}: {c.replicates}个重复" for g, c in params.gene_configs.items()]
                            gene_configs_info = f"，特殊配置: {', '.join(configs)}"
                        
                        gene_info = f"已选择 {len(selected_genes)} 个基因{gene_configs_info}"
                        
                        yield f"data: {json.dumps({'type': 'text', 'content': f'参数解析完成，正在生成布局...'}, ensure_ascii=False)}\n\n"
                        await asyncio.sleep(0)
                    else:
                        # 回退到正则表达式提取
                        gene_count = agent_service.extract_gene_count(request.message, len(all_genes))
                        
                        if gene_count is not None and gene_count < len(all_genes):
                            selected_genes = all_genes[:gene_count]
                            wells_data = [w for w in wells_data if w.gene_symbol in set(selected_genes)]
                            gene_info = f"已选择前 {gene_count} 个基因: {', '.join(selected_genes)}"
                        else:
                            selected_genes = all_genes
                            gene_info = f"使用全部 {len(all_genes)} 个基因"
                        
                        params = agent_service.extract_parameters(request.message, request.history, len(selected_genes))
                    
                    source_plate = SourcePlate(
                        barcode=source_data.get('plateId') or source_data.get('barcode', 'SOURCE_PLATE'),
                        wells=wells_data
                    )
                    
                    print(f"[DEBUG] Source plate: {source_plate.barcode}, wells: {len(source_plate.wells)}, genes: {len(source_plate.get_genes())}, plate_type: {params.plate_type}")
                    print(f"[DEBUG] Gene configs: {params.gene_configs}")
                    
                    # 生成布局
                    result = layout_service.generate_layout(
                        source_plate=source_plate,
                        params=params
                    )
                    
                    if result.status == SolveStatus.SUCCESS or result.status == SolveStatus.PARTIAL:
                        # 转换布局为前端格式
                        layout = result.layouts[0] if result.layouts else None
                        if layout:
                            frontend_layout = {
                                'layoutId': f'layout_{layout.plate_index}',
                                'plateFormat': layout.plate_type.value,
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
                            
                            # 发送布局数据
                            yield f"data: {json.dumps({'type': 'layout', 'content': frontend_layout}, ensure_ascii=False)}\n\n"
                            await asyncio.sleep(0)
                            
                            plate_info = f"{params.plate_type.value}孔板"
                            
                            # 计算总样本数
                            total_samples = sum(params.get_replicates_for_gene(g) for g in selected_genes)
                            
                            # 构建详细的配置信息
                            if params.gene_configs:
                                special_configs = [f"{g}({c.replicates}次)" for g, c in params.gene_configs.items()]
                                config_detail = f"，特殊配置: {', '.join(special_configs)}"
                            else:
                                config_detail = ""
                            
                            msg = f'\n\n✅ 布局生成成功！{gene_info}，默认每个基因 {params.replicates} 个重复{config_detail}，总样本数 {total_samples}，使用 {plate_info}。已在左侧显示。'
                            yield f"data: {json.dumps({'type': 'text', 'content': msg}, ensure_ascii=False)}\n\n"
                        else:
                            msg = '\n\n❌ 布局生成失败，请检查参数。'
                            yield f"data: {json.dumps({'type': 'text', 'content': msg}, ensure_ascii=False)}\n\n"
                    else:
                        msg = f'\n\n❌ {result.message}'
                        yield f"data: {json.dumps({'type': 'text', 'content': msg}, ensure_ascii=False)}\n\n"
                        
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
