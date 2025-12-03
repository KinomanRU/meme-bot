import asyncio
import logging
from os import getenv
import importlib.util
from datetime import datetime
from aiogram import Bot, Dispatcher
import log_utils
import proxy_utils
from routers import router as main_router

if importlib.util.find_spec("dotenv"):
    from dotenv import load_dotenv

    load_dotenv()

log = logging.getLogger(name=__name__)


async def main() -> None:
    log_utils.init_logging()
    bot_token = getenv("BOT_TOKEN")
    if not bot_token:
        raise Exception("BOT_TOKEN environment variable is not set")
    dp = Dispatcher()
    dp.include_router(main_router)
    bot = Bot(
        token=bot_token,
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
