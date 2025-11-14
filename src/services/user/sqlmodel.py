from typing import Optional
from typing import Unpack
from uuid import UUID

from lib.repos.abc import Repository

from .abc import UserRegisterData
from .abc import UserService
from .exceptions import AlreadyExistError
from models import UserModel


class SQLModelUserService(UserService[UserModel]):
    """Service for user data manipulation"""

    def __init__(self, user_repo: Repository[UserModel, UUID]) -> None:
        self.user_repo = user_repo

    async def register(self, **kwargs: Unpack[UserRegisterData]) -> UUID:
        """
        Args:
            :telegram_id: int   # user id in telegram
        Return:
            :user_id: UUID  # user id in DB
        """
        telegram_id = kwargs.get("telegram_id")

        user_exist = await self.get(telegram_id=telegram_id)
        if user_exist:
            raise AlreadyExistError(
                "User with telegram_id=%r already exist" % telegram_id)

        new_user = UserModel(telegram_id=telegram_id)
        user_id = await self.user_repo.add(new_user)
        await self.user_repo.commit()
        return user_id

    async def get(
            self,
            id: Optional[UUID] = None,
            telegram_id: Optional[int] = None,
            ) -> UserModel | None:
        """
        Args:
            :id: Optional[UUID]   # user's id in DB
            :telegram_id: Optional[int]   # user's id in telegram
        Return:
            :user: User | None
        """
        properties = {}

        if id is None and telegram_id is None:
            return None

        if id is not None:
            properties["id"] = id

        if telegram_id is not None:
            properties["telegram_id"] = telegram_id

        return await self.user_repo.get_one(**properties)

    async def is_registered(self, telegram_id: int) -> bool:
        """
        Args:
            :telegram_id: int   # user's telegram id
        Return:
            :is_user_registered: bool
        """
        return not not await self.get(telegram_id=telegram_id)
