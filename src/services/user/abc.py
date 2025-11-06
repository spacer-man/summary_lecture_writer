from typing import Optional
from typing import Protocol
from typing import TypedDict
from typing import Unpack
from uuid import UUID


class UserRegisterData(TypedDict):
    telegram_id: int


class UserService[User](Protocol):
    """Service for user data manipulation"""
    async def register(self, **kwargs: Unpack[UserRegisterData]) -> UUID:
        """
        Args:
            :telegram_id: int   # user id in telegram
        Return:
            :user_id: UUID  # user id in DB
        """
        ...
    async def get(
            self,
            id: Optional[UUID] = None,
            telegram_id: Optional[int] = None,
            ) -> User | None:
        """
        Args:
            :id: Optional[UUID]   # user's id in DB
            :telegram_id: Optional[int]   # user's id in telegram
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
