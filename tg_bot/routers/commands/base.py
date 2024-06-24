import asyncio
import logging

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

import config as cfg
import log_utils

log = logging.getLogger(name=__name__)
router = Router(name=__name__)


@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    log.info(log_utils.format_message(message=message))
    await asyncio.sleep(0.05)
    await message.answer(
        text=f"Hello, {message.from_user.full_name}!\n\n" + cfg.HELP_TEXT
    )


@router.message(Command("help"))
async def handle_help(message: Message) -> None:
    log.info(log_utils.format_message(message=message))
    await asyncio.sleep(0.05)
    await message.answer(text=cfg.HELP_TEXT)
