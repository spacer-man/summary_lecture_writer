from pydantic import Field
from pydantic import SecretStr

from .env import BaseEnvConfig


class DBConfig(BaseEnvConfig):
    url: SecretStr = Field(alias="DB_URL")
