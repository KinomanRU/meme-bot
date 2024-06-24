import asyncio
import logging

from aiogram import Router
from aiogram.types import Message

import config as cfg
import log_utils

log = logging.getLogger(name=__name__)
router = Router(name=__name__)


@router.message()
async def echo_message(message: Message) -> None:
    log.info(log_utils.format_message(message=message))
    await asyncio.sleep(0.05)
    await message.reply(text=cfg.INCORRECT_INPUT_TEXT)
