from typing import Optional
from typing import Protocol
from typing import TypedDict
from typing import Unpack
from uuid import UUID


class UserRegisterData(TypedDict):
    telegram_id: int


class UserService[User](Protocol):
    """Service for user data manipulation"""
    async def register(self, **kwargs: Unpack[UserRegisterData]) -> None:
        """
        Args:
            :telegram_id: user id in telegram
        Return:
            :nothing: None
        """
        ...
    async def get(
            self,
            id: Optional[UUID] = None,
            telegram_id: Optional[int] = None,
            ) -> User | None:
        """
        Args:
            :id: user's id in DB
            :telegram_id: user's id in telegram
        Return:
            :user: User | None
        """
        ...
    async def is_registered(self, telegram_id: int) -> bool:
        """
        Args:
            :telegram_id: int   # user's telegram id
        Return:
            :is_user_registered: bool
        """
        ...
