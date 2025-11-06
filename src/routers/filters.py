from aiogram.filters import BaseFilter
from aiogram.types import Message

from services.user.abc import UserService


def new_is_registered_filer(user_service: UserService):
    class IsRegisteredFilter(BaseFilter):
        def __init__(self, need_registered: bool = True) -> None:
            self.need_registered = need_registered

        async def __call__(
                self,
                message: Message,
                ) -> bool:
            user_telegram_id = message.chat.id
            return self.need_registered == user_service.is_registered(
                telegram_id=user_telegram_id)

    return IsRegisteredFilter
