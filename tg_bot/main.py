import asyncio
import logging
from typing import Never
from aiogram import Bot, Dispatcher
import log_utils
import proxy_utils
from routers import router as main_router
from datetime import datetime as dt
from config import config

log = logging.getLogger(name=__name__)


async def main() -> Never:
    log_utils.init_logging()
    dp = Dispatcher()
    dp.include_router(main_router)
    bot = Bot(
        token=config.get("Bot", "Bot_Token"),
        session=proxy_utils.SESSION,
    )
    print(dt.now(), "Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    print(dt.now(), "Starting...")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("Normal shutdown")
        print(dt.now(), "Bot stopped")
    except Exception as err:
        log.exception(str(err))
