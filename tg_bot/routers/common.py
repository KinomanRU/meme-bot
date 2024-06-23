import log_utils
import logging
import asyncio
from aiogram import Router, types
from config import INCORRECT_INPUT_TEXT

log = logging.getLogger(name=__name__)
router = Router(name=__name__)


@router.message()
async def echo_message(message: types.Message) -> None:
    log.info(log_utils.format_message(message=message))
    await asyncio.sleep(0.05)
    await message.reply(text=INCORRECT_INPUT_TEXT)
