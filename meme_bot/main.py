import asyncio
import logging
from datetime import datetime

import log_utils
import proxy_utils
from aiogram import Bot, Dispatcher
from config import config
from errors import BotNoToken
from request_utils import http_client
from routers import router as main_router

log = logging.getLogger(__name__)


async def main() -> None:
    log_utils.init_logging()
    bot_token = config.bot_token
    if not bot_token:
        raise BotNoToken
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
    except Exception:
        log.exception("An error has occurred")
    finally:
        print(datetime.now(), "Bot stopped")
