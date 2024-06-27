import logging
from aiogram import Router
from aiogram.enums import ChatAction
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import log_utils
import strings

log = logging.getLogger(name=__name__)
router = Router(name=__name__)


@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    log.info(log_utils.format_message(message=message))
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    )
    await message.answer(
        text=strings.HELLO.replace("%USER%", message.from_user.full_name)
    )


@router.message(Command("help"))
async def handle_help(message: Message) -> None:
    log.info(log_utils.format_message(message=message))
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    )
    await message.answer(text=strings.HELP)
