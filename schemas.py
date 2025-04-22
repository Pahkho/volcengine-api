from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class ImageGenerationRequest(BaseModel):
    req_key: str = "high_aes_general_v21_L"
    width: int = 512
    height: int = 512
    seed: int = -1
    prompt: str
    model_version: str = "general_v2.0_L"
    req_schedule_conf: str = "general_v20_9B_rephraser"
    negative_prompt: str = "nsfw, nude, smooth skin, unblemished skin, mole, low resolution, blurry, worst quality, mutated hands"
    scale: float = 3.5
    ddim_steps: int = 16
    use_pre_llm: bool = True
    use_sr: bool = True
    sr_seed: int = -1
    is_only_sr: bool = False
    sr_scale: float = 3.5
    sr_steps: int = 10
    sr_strength: float = 0.4
    # return_url: bool = True
    # logo_info: dict = {
    #     "add_logo": False,
    #     "position": 0,
    #     "language": 0,
    #     "opacity": 0.3
    # }

# 定义 LogoInfo 模型
class LogoInfo(BaseModel):
    add_logo: bool
    position: int
    language: int
    logo_text_content: str

class TaskRequest(BaseModel):
    req_key: str = "high_aes_general_v21_L"
    task_id: str
    req_json: Optional[str] = None

# 添加或修改ImageGenerationResponse模型
class ImageGenerationResponse(BaseModel):
    ResponseMetadata: Optional[Dict[str, Any]] = None
    code: int
    message: str
    request_id: str
    time_elapsed: str
    data: Dict[str, Any]

# 定义 ResponseMetadata 模型
class ResponseMetadataModel(BaseModel):
    status: str
    timestamp: str
    additional_info: Optional[Dict[str, Any]] = None

# 定义 ErrorInfo 模型
class ResponseErrorInfoModel(BaseModel):
    Code: str
    Message: str