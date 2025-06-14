import logging
from aiogram import Router
from aiogram.enums import ChatAction
from aiogram.filters import Command
from aiogram.types import Message
import log_utils
import strings
from anecdote import get_anecdote
from meme import get_meme_link

log = logging.getLogger(name=__name__)
router = Router(name=__name__)


@router.message(Command("anec"))
async def handle_anecdote(message: Message) -> None:
    log_utils.log_command(log, logging.INFO, message)
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    )
    anecdote_text: str = await get_anecdote()
    if anecdote_text:
        await message.answer(text=anecdote_text)
    else:
        await message.answer(text=strings.CONTENT_ERROR)


@router.message(Command("meme"))
async def handle_meme(message: Message) -> None:
    log_utils.log_command(log, logging.INFO, message)
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_DOCUMENT,
    )
    meme_url: str = await get_meme_link()
    if meme_url.startswith("http"):
        match meme_url.split(".")[-1]:
            case "gif":
                await message.answer_animation(animation=meme_url)
            case "mp4":
                await message.answer_video(video=meme_url)
            case _:
                await message.answer_photo(photo=meme_url)
    elif meme_url:
        await message.answer(text=meme_url)
    else:
        await message.answer(text=strings.CONTENT_ERROR)


@router.message(Command("gmeme"))
async def handle_vmeme(message: Message) -> None:
    log_utils.log_command(log, logging.INFO, message)
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_DOCUMENT,
    )
    meme_url: str = await get_meme_link("gif")
    if meme_url.startswith("http"):
        await message.answer_animation(animation=meme_url)
    elif meme_url:
        await message.answer(text=meme_url)
    else:
        await message.answer(text=strings.CONTENT_ERROR)


@router.message(Command("vmeme"))
async def handle_gmeme(message: Message) -> None:
    log_utils.log_command(log, logging.INFO, message)
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_VIDEO,
    )
    meme_url: str = await get_meme_link("video")
    if meme_url.startswith("http"):
        await message.answer_video(video=meme_url)
    elif meme_url:
        await message.answer(text=meme_url)
    else:
        await message.answer(text=strings.CONTENT_ERROR)
