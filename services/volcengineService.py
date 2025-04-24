import requests
from fastapi import HTTPException
from config import logger, volcengine_config
from volcengine import visual
from volcengine.visual.VisualService import VisualService
import logging


def create_visual_service():
    visual_service = VisualService()
    # 从配置获取AK/SK
    visual_service.set_ak(volcengine_config.AK)
    visual_service.set_sk(volcengine_config.SK)
    return visual_service


def sync2async_submit(form: dict):
    try:
        visual_service = create_visual_service()
        response = visual_service.cv_sync2async_submit_task(form)
        # 新增调试输出，确保获取到正确的字段
        # response_data = response.json()
        # print(f"response_data: {response_data}")  # 新增调试输出

        # if response.status != 10000:
        #     raise HTTPException(status_code=response.status_code,
        #                         detail=f"Failed to create session: {response.text}")

        # print(f"task_id: {response_data.get('data', {}).get('task_id')}")  # 新增调试输出
        # 根据实际响应结构调整字段路径（示例假设task_id在data字段中）
        return response.get('data', {}).get('task_id')  # 修改字段路径
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Network error: {str(e)}")


def sync2async_get(form: dict):
    try:
        visual_service = create_visual_service()
        response = visual_service.cv_sync2async_get_result(form)

        # if response.status_code != 200:
        #     raise HTTPException(status_code=response.status_code,
        #                         detail=f"Failed to query task: {response.text}")

        # 解析响应数据为JSON
        # result = response.json()
        # 新增调试输出，确保获取到正确的字段
        # print(f"result: {result}")  # 新增调试输出
        return response  # 返回JSON数据而不是response对象
    except requests.JSONDecodeError as e:
        # logger.error(f"JSON解析失败: {response.text}")
        raise HTTPException(status_code=500, detail="Invalid JSON response")
    except Exception as e:
        logger.error(f"解析失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"解析错误: {str(e)}")