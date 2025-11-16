from pydantic import Field

from .env import BaseEnvConfig


class STTConfig(BaseEnvConfig):
#     model_path: str = Field(alias="STT_MODEL_PATH")
    server_url: str = Field(alias="STT_SERVER_URL")
