import asyncio
import logging
from datetime import datetime
from typing import Never
from aiogram import Bot, Dispatcher
import log_utils
import proxy_utils
from config import config
from routers import router as main_router

log = logging.getLogger(name=__name__)


async def main() -> Never:
    log_utils.init_logging()
    dp = Dispatcher()
    dp.include_router(main_router)
    bot = Bot(
        token=config.get("Bot", "Bot_Token"),
        session=proxy_utils.SESSION,
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    print(datetime.now(), "Bot started")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("Normal shutdown")
    except Exception as err:
        log.exception(str(err))
    finally:
        print(datetime.now(), "Bot stopped")
