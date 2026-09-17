import logging

import log_utils
import strings
from aiogram import Router
from aiogram.enums import ChatAction
from aiogram.types import Message

log = logging.getLogger(name=__name__)
router = Router(name=__name__)


@router.message()
async def echo_message(message: Message) -> None:
    log_utils.log_command(log, logging.INFO, message)
    if message.bot:
        await message.bot.send_chat_action(
            chat_id=message.chat.id,
            action=ChatAction.TYPING,
        )
    await message.reply(text=strings.UNKNOWN_COMMAND)
