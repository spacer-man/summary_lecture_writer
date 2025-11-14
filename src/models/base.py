from typing import Optional
from uuid import UUID

from sqlmodel import SQLModel
from pydantic import Field


class BaseModel(SQLModel):
    ...


class BaseUUIDModel(BaseModel):
    id: Optional[UUID] = Field(default=None)
