from typing import Optional
from uuid import UUID

from pydantic import BaseModel as BasePydanticModel
from pydantic import Field


class BaseModel(BasePydanticModel):
    ...


class BaseUUIDModel(BaseModel):
    id: Optional[UUID] = Field(default=None)
