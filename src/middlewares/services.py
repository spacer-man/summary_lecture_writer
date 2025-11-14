from typing import Any
from typing import Awaitable
from typing import Callable
from typing import Dict

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession

import db


class DBServicesMiddleware(BaseMiddleware):
    def __init__(
            self,
            services: dict[str, Callable[[AsyncSession], Any]],
            ) -> None:
        self.services = services

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
        ) -> Any:  # pragma: no cover
        async with db.new_db_session() as session:
            for service_name, service_gen in self.services.items():
                data[service_name] = service_gen(session)
            await handler(event, data)
