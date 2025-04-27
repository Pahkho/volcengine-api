from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class ImageGenerationRequest(BaseModel):
    req_key: str = Field("high_aes_general_v21_L", description="请求密钥，默认为 high_aes_general_v21_L")
    width: int = Field(512, description="生成图像的宽度，默认为 512")
    height: int = Field(512, description="生成图像的高度，默认为 512")
    seed: int = Field(-1, description="随机种子，默认为 -1")
    prompt: str = Field(..., description="生成图像的提示词，必填项")
    model_version: str = Field("general_v2.0_L", description="使用的模型版本，默认为 general_v2.0_L")
    req_schedule_conf: str = Field("general_v20_9B_rephraser",description="请求调度配置，默认为 general_v20_9B_rephraser")
    negative_prompt: str = Field(
        "nsfw, nude, smooth skin, unblemished skin, mole, low resolution, blurry, worst quality, mutated hands",
        description="负向提示词，默认为指定内容")
    scale: float = Field(3.5, description="缩放比例，默认为 3.5")
    ddim_steps: int = Field(16, description="DDIM 步数，默认为 16")
    use_pre_llm: bool = Field(True, description="是否使用预训练大语言模型，默认为 True")
    use_sr: bool = Field(True, description="是否使用超分辨率，默认为 True")
    sr_seed: int = Field(-1, description="超分辨率的随机种子，默认为 -1")
    is_only_sr: bool = Field(False, description="是否仅进行超分辨率处理，默认为 False")
    sr_scale: float = Field(3.5, description="超分辨率的缩放比例，默认为 3.5")
    sr_steps: int = Field(10, description="超分辨率的步数，默认为 10")
    sr_strength: float = Field(0.4, description="超分辨率的强度，默认为 0.4")
    req_json: dict = Field({
        "return_url": True,
        "logo_info": {
            "add_logo": False,
            "position": 0,
            "language": 0,
            "opacity": 0.3,
            "logo_text_content": "这是水印"
        }
    }, description="请求的 JSON 配置，包含返回 URL 和水印信息等")


# 定义 LogoInfo 模型
class LogoInfo(BaseModel):
    add_logo: bool = Field(..., description="是否添加水印，必填项")
    position: int = Field(..., description="水印的位置，必填项")
    language: int = Field(..., description="水印的语言，必填项")
    logo_text_content: str = Field(..., description="水印的文本内容，必填项")


class TaskRequest(BaseModel):
    req_key: str = Field("high_aes_general_v21_L", description="请求密钥，默认为 high_aes_general_v21_L")
    task_id: str = Field(..., description="任务 ID，必填项")
    req_json: Optional[str] = Field(None, description="请求的 JSON 字符串，可选字段")


# 添加或修改ImageGenerationResponse模型
class ImageGenerationResponse(BaseModel):
    ResponseMetadata: Optional[Dict[str, Any]] = Field(None, description="响应的元数据，可选字段")
    code: int = Field(..., description="响应的状态码，必填项")
    message: str = Field(..., description="响应的消息内容，必填项")
    request_id: str = Field(..., description="请求的 ID，必填项")
    time_elapsed: str = Field(..., description="请求所花费的时间，必填项")
    data: Dict[str, Any] = Field(..., description="响应的数据，必填项")


# 定义 ResponseMetadata 模型
class ResponseMetadataModel(BaseModel):
    status: str = Field(..., description="响应的状态，必填项")
    timestamp: str = Field(..., description="响应的时间戳，必填项")
    additional_info: Optional[Dict[str, Any]] = Field(None, description="额外的信息，可选字段")


# 定义 ErrorInfo 模型
class ResponseErrorInfoModel(BaseModel):
    Code: str = Field(..., description="错误码，必填项")
    Message: str = Field(..., description="错误消息，必填项")
