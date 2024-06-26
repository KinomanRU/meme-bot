import logging
from aiogram import Router
from aiogram.enums import ChatAction
from aiogram.types import Message
import log_utils
import strings

log = logging.getLogger(name=__name__)
router = Router(name=__name__)


@router.message()
async def echo_message(message: Message) -> None:
    log.info(log_utils.format_message(message=message))
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    )
    await message.reply(text=strings.UNKNOWN_COMMAND)
