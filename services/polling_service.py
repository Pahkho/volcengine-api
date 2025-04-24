import asyncio
from typing import Callable, Any, Optional, Dict
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

class PollingService:
    def __init__(
        self,
        max_retries: int = 30,
        retry_interval: float = 2.0,
        success_condition: Optional[Callable[[Dict], bool]] = None
    ):
        self.max_retries = max_retries
        self.retry_interval = retry_interval
        self.success_condition = success_condition or self._default_success_condition

    @staticmethod
    def _default_success_condition(response: Dict) -> bool:
        """默认的成功条件检查"""
        return (
            # response.get("status") == "success" or
            response.get("data", {}).get("status") == "done"
        )

    @staticmethod
    def _is_failed(response: Dict) -> bool:
        """检查任务是否失败"""
        return (
            # response.get("status") == "failed" or
            response.get("data", {}).get("status") == "not_found"
        )

    async def poll_until_complete(
        self,
        query_func: Callable[..., Any],
        query_params: Dict,
        error_message: str = "Task processing failed"
    ) -> Dict:
        """
        轮询直到任务完成
        
        Args:
            query_func: 查询函数
            query_params: 查询参数
            error_message: 错误消息
            
        Returns:
            Dict: 任务结果
            
        Raises:
            HTTPException: 当任务失败或超时时
        """
        for attempt in range(self.max_retries):
            try:
                result = query_func(query_params)
                
                # 检查是否成功
                if self.success_condition(result):
                    return result
                
                # 检查是否失败
                if self._is_failed(result):
                    logger.error(f"Task failed: {result}")
                    raise HTTPException(
                        status_code=500,
                        detail=error_message
                    )
                
                # 如果既不是成功也不是失败，则等待后重试
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_interval)
                    
            except Exception as e:
                logger.error(f"Error during polling: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Polling error: {str(e)}"
                )
        
        # 如果达到最大重试次数
        raise HTTPException(
            status_code=408,
            detail="Task timeout after maximum retries"
        )