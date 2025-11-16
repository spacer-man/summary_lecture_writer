from typing import Optional
from uuid import UUID

from sqlmodel import Field
from sqlmodel import SQLModel
from uuid_extensions import uuid7


class BaseModel(SQLModel):
    ...


class BaseUUIDModel(BaseModel):
    id: Optional[UUID] = Field(default_factory=uuid7, primary_key=True)
