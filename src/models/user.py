from .base import BaseUUIDModel


class UserModel(BaseUUIDModel):
    """User model for DB relation"""
    telegram_id: int    # = Field(unicue=True)
