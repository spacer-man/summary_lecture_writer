from pydantic import Field

from .env import BaseEnvConfig


class RedisConfig(BaseEnvConfig):
    url: str = Field(alias="REDIS_URL")
