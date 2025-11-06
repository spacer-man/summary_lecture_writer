from aiogram import Router
from aiogram.types import Message
from aiogram.filters import StateFilter

from routers.greeting import messages
from services.user.abc import UserService


greeting_router = Router(name="greeting")


@greeting_router.message(StateFilter(None))
async def first_greeting(
        message: Message,
        user_service: UserService,
        ) -> None:
    user_telegram_id = message.chat.id
    await message.answer(text=messages.FIRST_GREETING)
    await user_service.register(telegram_id=user_telegram_id)


@greeting_router.message(StateFilter(None))
async def main_menu(message: Message) -> None:
    await message.answer(text=messages.MAIN_MENU)
