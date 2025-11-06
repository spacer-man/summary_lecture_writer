from aiogram import Router

from .greeting import greeting_router
from .summarise import summarise_router


main_router = Router(name="main")

routers = [
    greeting_router,
    summarise_router,
]
main_router.include_routers(*routers)


__all__ = ["main_router"]
