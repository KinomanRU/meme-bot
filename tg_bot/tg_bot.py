import asyncio
import logging
from typing import Never

from aiogram import Bot, Dispatcher

import config as cfg
import log_utils
from routers import router as main_router

log = logging.getLogger(name=__name__)


async def main() -> Never:
    log_utils.init_logging()
    dp = Dispatcher()
    dp.include_router(main_router)
    bot = Bot(
        token=cfg.BOT_TOKEN,
        session=cfg.session,
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("Normal shutdown")
    except Exception as err:
        log.exception(str(err))
