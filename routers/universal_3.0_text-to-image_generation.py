import re
from typing import Dict, Any

from fastapi import APIRouter, HTTPException

from schemas import ImageGenerationResponse, ImageGenerationRequest
from volcengine import visual
from volcengine.visual.VisualService import VisualService

router = APIRouter()

@router.post("/text_to_image_3V", response_model= ImageGenerationResponse)
async def text_to_image_3V(request: ImageGenerationRequest):

    """将自然语言转换为SQL的API端点"""
    visual_service = VisualService()
    # 设置AK/SK，需替换为真实值
    visual_service.set_ak('AKLTOTc1OWViNTFlN2Y1NDgwZTliM2VmNDc4N2M2ZDE3ODA')
    visual_service.set_sk('TTJGalpqQmpZVEUyTW1JM05EZzRPRGcxWkdZd09XTmpNelppT1dNME9EQQ==')

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

    try:
        # 2. 发送查询(同步转异步)
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