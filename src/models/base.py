from typing import Optional
from uuid import UUID

from sqlmodel import Field
from sqlmodel import SQLModel


class BaseModel(SQLModel):
    ...


class BaseUUIDModel(BaseModel):
    id: Optional[UUID] = Field(default=None, primary_key=True)
