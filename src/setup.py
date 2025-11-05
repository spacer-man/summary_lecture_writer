from aiogram import Bot
from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.enums import UpdateType
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage

from configs.bot import BotConfig
from configs.bot import StateStorageType


def state_storage() -> BaseStorage:
    config = BotConfig()

    match config.state_storage_type:
        case StateStorageType.redis:
            from configs.redis import RedisConfig
            redis_config = RedisConfig()

            storage = RedisStorage.from_url(
                url=redis_config.url)

        case _:
            storage = MemoryStorage()

    return storage


def bot() -> Bot:
    config = BotConfig()
    return Bot(
        token=config.token.get_secret_value(),
        default=DefaultBotProperties(
            parse_mode=ParseMode.MARKDOWN,
            disable_notification=False))


def dispatcher() -> Dispatcher:
    return Dispatcher(
        storage=None,
        name="main")


allowed_updates = [
    UpdateType.MESSAGE,
]
