import re
from typing import Dict, Any

from fastapi import APIRouter, HTTPException

from schemas import ImageGenerationResponse, ImageGenerationRequest
from volcengine import visual
from volcengine.visual.VisualService import VisualService

from config import volcengine_config

router = APIRouter()

@router.post("/image", response_model=ImageGenerationResponse)
async def image_generation(request: ImageGenerationRequest):
    """将自然语言转换为SQL的API端点"""
    visual_service = VisualService()
    # 从配置获取AK/SK
    visual_service.set_ak('AKLTMGRjY2MzMWE4MDdlNDI5MDg0OGQzZDhiMDUwOWFkOGM')
    visual_service.set_sk('TkdNd1lqaGhNakptT0ROa05Ea3lZVGc1WmpreVpqUXdOMlE1WVRVeVlUTQ==')
    
    form = build_request_form(request)

    try:
        # 2. 发送查询
        result = visual_service.cv_sync2async_submit_task(form)
        # 3. 构造响应
        return result
    except HTTPException as he:
        raise he
    except Exception as e:
        # Log the exception details for debugging
        print(f"Error in image generation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

def build_request_form(request: ImageGenerationRequest) -> Dict[str, Any]:
    """根据请求构建API调用参数"""
    form = {
        "req_key": request.req_key,
        "prompt": request.prompt,
        "width": request.width,
        "height": request.height,
        "seed": request.seed,
        "model_version": request.model_version,
        "req_schedule_conf": request.req_schedule_conf,
        "negative_prompt": request.negative_prompt,
        "scale": request.scale,
        "ddim_steps": request.ddim_steps,
        "use_pre_llm": request.use_pre_llm,
        "use_sr": request.use_sr,
        "sr_seed": request.sr_seed,
        "is_only_sr": request.is_only_sr,
        "sr_scale": request.sr_scale,
        "sr_steps": request.sr_steps,
        "sr_strength": request.sr_strength
    }
    
        
    return form