import json
import re
from typing import Dict, Any

from fastapi import APIRouter, HTTPException
from config import volcengine_config
from schemas import ImageGenerationResponse, ImageGenerationRequest, TaskRequest
from volcengine import visual
from volcengine.visual.VisualService import VisualService

router = APIRouter()

@router.post("/queryTask", response_model= ImageGenerationResponse)
async def query_task(request: TaskRequest):

    visual_service = VisualService()
    # 设置AK/SK，需替换为真实值
    visual_service.set_ak(volcengine_config.AK)
    visual_service.set_sk(volcengine_config.SK)

    # if request.req_json:
    #     req_json = json.loads(request.req_json)
    # else:
    #     req_json = {}

    form = {
        "req_key": request.req_key,
        "task_id": request.task_id,
        "req_json": request.req_json,
    }

    try:
        # 2. 发送查询
        result = visual_service.cv_sync2async_get_result(form)
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