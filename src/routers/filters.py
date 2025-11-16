from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.types import User

from services.user.abc import UserService


class IsRegisteredFilter(BaseFilter):
    def __init__(self, should_be_registered: bool = True) -> None:
        self.should_be = should_be_registered

    async def __call__(
            self,
            _: Message,
            event_from_user: User,
            user_service: UserService,
            ) -> bool:
        return self.should_be == await user_service.is_registered(
            telegram_id=event_from_user.id)
