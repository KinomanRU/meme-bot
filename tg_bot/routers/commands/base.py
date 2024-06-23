import log_utils
import logging
import asyncio
from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from config import HELP_TEXT

log = logging.getLogger(name=__name__)
router = Router(name=__name__)


@router.message(CommandStart())
async def handle_start(message: types.Message) -> None:
    log.info(log_utils.format_message(message=message))
    await asyncio.sleep(0.05)
    await message.answer(text=f"Hello, {message.from_user.full_name}!\n\n" + HELP_TEXT)


@router.message(Command("help"))
async def handle_help(message: types.Message) -> None:
    log.info(log_utils.format_message(message=message))
    await asyncio.sleep(0.05)
    await message.answer(text=HELP_TEXT)
