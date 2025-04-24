import re
from typing import Dict, Any

from fastapi import APIRouter, HTTPException
from config import volcengine_config
from schemas import ImageGenerationResponse, ImageGenerationRequest
from volcengine import visual
from volcengine.visual.VisualService import VisualService
from services.volcengineService import sync2async_submit, sync2async_get
import json
import logging
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/text_to_image_2v", response_model= ImageGenerationResponse)
async def text_to_image_2v(request: ImageGenerationRequest):

    req_key = request.req_key

    request_form = {
        "req_key": req_key,
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
        result = sync2async_submit(request_form)

        task_form = {
            "req_key": req_key,
            "task_id": result,
            "req_json": json.dumps(request.req_json) if request.req_json else json.dumps({})
        }

        task_result = sync2async_get(task_form)
        # 3. 构造响应
        return task_result
    except HTTPException as he:
        raise he
    except Exception as e:
        # Log the exception details for debugging
        logger.error(f"Error in image generation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )