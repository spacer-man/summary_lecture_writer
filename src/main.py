import asyncio
import logging

import logs
import setup


log = logging.getLogger(__name__)


async def main():
    bot = setup.bot()
    dp = setup.dispatcher()
    try:
        await dp.start_polling(
            bot,
            allowed_updates=setup.allowed_updates)
    except Exception as err:
        log.error("Polling error: %r", err, exc_info=True)


if __name__ == "__main__":
    logs.setup_logs()
    asyncio.run(main())
