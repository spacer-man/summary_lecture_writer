from sqlmodel import Field

from .base import BaseUUIDModel


class UserModel(BaseUUIDModel, table=True):
    """User model for DB relation"""
    telegram_id: int = Field(unique=True)
