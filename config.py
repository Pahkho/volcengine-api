import logging
import os
from dotenv import load_dotenv

# 日志配置
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("volcengine-proxy")


# 加载.env文件
load_dotenv()

# 火山引擎配置
class VolcengineConfig:
    AK = os.getenv('VOLCENGINE_AK')
    SK = os.getenv('VOLCENGINE_SK')

    @classmethod
    def validate(cls):
        if not cls.AK or not cls.SK:
            raise ValueError("未设置火山引擎AK/SK")

# 创建配置实例
volcengine_config = VolcengineConfig()