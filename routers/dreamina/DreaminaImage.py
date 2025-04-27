from fastapi import APIRouter, HTTPException

from schemas.DreaminaSchemas import DreaminaRequest
from schemas.schemas import ImageGenerationResponse

from services.pollingService import PollingService
from services.volcengineService import sync2async_submit, sync2async_get
import json
import logging
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/dreaminaImage", response_model= ImageGenerationResponse)
async def dreamina_image(request: DreaminaRequest):



    request_form = {
        "req_key": "jimeng_high_aes_general_v21_L",
        "prompt": request.prompt,
        "seed": request.seed,
        "width": request.width,
        "height": request.height,
        "use_pre_llm": request.use_pre_llm,
        "use_sr": request.use_sr
    }

    try:
        # 2. 发送查询(同步转异步)
        result = sync2async_submit(request_form)

        task_form = {
            "req_key": "jimeng_high_aes_general_v21_L",
            "task_id": result,
            # "req_json": json.dumps(request.req_json) if isinstance(request.req_json, dict) else (request.req_json if isinstance(request.req_json, str) else json.dumps({}))
            "req_json": "{\"logo_info\":{\"add_logo\":true,\"position\":0,\"language\":0,\"logo_text_content\":\"这里是明水印内容\"},\"return_url\":true}"
        }

        # 创建轮询服务实例
        polling_service = PollingService(
            max_retries=10,  # 最大重试30次
            retry_interval=2.0  # 每次间隔2秒
        )

        # 使用轮询服务等待结果
        task_result = await polling_service.poll_until_complete(
            query_func=sync2async_get,
            query_params=task_form,
            error_message="Image generation task failed"
        )

        # task_result = sync2async_get(task_form)
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