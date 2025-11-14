from pydantic import Field
from pydantic import SecretStr

from .env import BaseEnvConfig


class RedisConfig(BaseEnvConfig):
    url: SecretStr = Field(alias="REDIS_URL")
