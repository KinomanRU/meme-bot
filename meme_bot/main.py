import asyncio
import logging
from datetime import datetime

import log_utils
import proxy_utils
from aiogram import Bot, Dispatcher
from config import config
from request_utils import http_client
from routers import router as main_router

log = logging.getLogger(name=__name__)


async def main() -> None:
    log_utils.init_logging()
    bot_token = config.bot_token
    if not bot_token:
        raise Exception("BOT_TOKEN environment variable is not set")
    dp = Dispatcher()
    dp.include_router(main_router)
    bot = Bot(
        token=bot_token,
        session=proxy_utils.SESSION,
    )
    try:
        await dp.start_polling(bot)
    finally:
        await http_client.close()


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
