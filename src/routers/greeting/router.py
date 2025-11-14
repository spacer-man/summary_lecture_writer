import logging

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import StateFilter

from routers.filters import IsRegisteredFilter
from routers.greeting import messages
from services.user.abc import UserService


greeting_router = Router(name="greeting")
log = logging.getLogger(__name__)


@greeting_router.message(StateFilter(None), IsRegisteredFilter(False))
async def first_greeting(
        message: Message,
        user_service: UserService,
        ) -> None:
    event_id = message.message_id
    user_telegram_id = message.chat.id

    await message.answer(text=messages.FIRST_GREETING)
    log.debug({
        "event_id": event_id,
        "message": "New user registration process...",
        "telegram_id": user_telegram_id,
    })
    await user_service.register(telegram_id=user_telegram_id)
    log.info({
        "event_id": event_id,
        "message": "New user registered",
        "telegram_id": user_telegram_id,
    })


# @greeting_router.message(StateFilter(None), IsRegisteredFilter(True))
async def main_menu(message: Message) -> None:
    event_id = message.message_id
    user_telegram_id = message.chat.id

    await message.answer(text=messages.MAIN_MENU)
    log.debug({
        "event_id": event_id,
        "message": "Show main menu for user",
        "telegram_id": user_telegram_id,
    })
