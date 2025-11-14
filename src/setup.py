from aiogram import Bot
from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.enums import UpdateType
from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.strategy import FSMStrategy

from configs.bot import BotConfig
from configs.bot import StateStorageType
from lib.repos.sqlmodel import SQLModelRepository
from middlewares.services import DBServicesMiddleware
from models.user import UserModel
from services.user.sqlmodel import SQLModelUserService


def state_storage() -> BaseStorage:
    config = BotConfig()

    match config.state_storage_type:
        case StateStorageType.redis:
            from configs.redis import RedisConfig
            redis_config = RedisConfig()

            storage = RedisStorage.from_url(
                url=redis_config.url.get_secret_value())

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
    dp = Dispatcher(
        storage=state_storage(),
        fsm_strategy=FSMStrategy.USER_IN_CHAT,
        disable_fsm=False,
        name="main")

    dp.message.middleware.register(DBServicesMiddleware(
        services={
            "user_service": lambda db: SQLModelUserService(
                user_repo=SQLModelRepository(
                    model=UserModel,
                    session=db)),
        }))

    return dp


allowed_updates = [
    UpdateType.MESSAGE,
]
