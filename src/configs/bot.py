import enum
from typing import Optional

from pydantic import Field
from pydantic import SecretStr

from .env import BaseEnvConfig


class StateStorageType(enum.StrEnum):
    inmemory = "inmemory"
    redis = "redis"


class BotConfig(BaseEnvConfig):
    token: SecretStr = Field(alias="BOT_TOKEN")
    state_storage_type: Optional[StateStorageType] = Field(
            default=None, alias="BOT_STATE_STORAGE_TYPE")
