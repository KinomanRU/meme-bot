import log_utils
import logging
import asyncio
from aiogram import Router, types
from aiogram.enums import ChatAction
from aiogram.filters import Command
from config import CONTENT_ERROR_TEXT
from anecdote import get_anecdote
from meme import get_meme_link

log = logging.getLogger(name=__name__)
router = Router(name=__name__)


@router.message(Command("anec"))
async def handle_anecdote(message: types.Message) -> None:
    log.info(log_utils.format_message(message=message))
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    )
    await asyncio.sleep(0.05)
    anecdote_text: str = await get_anecdote()
    if anecdote_text:
        await message.answer(text=anecdote_text)
    else:
        await message.answer(text=CONTENT_ERROR_TEXT)


@router.message(Command("meme"))
async def handle_meme(message: types.Message) -> None:
    log.info(log_utils.format_message(message=message))
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING,
    )
    await asyncio.sleep(0.05)
    meme_url: str = await get_meme_link()
    if meme_url.startswith("http"):
        meme_ext: str = meme_url.split(".")[-1]
        if meme_ext == "gif":
            await message.answer_animation(animation=meme_url)
        elif meme_ext == "mp4":
            await message.answer_video(video=meme_url)
        else:
            await message.answer_photo(photo=meme_url)
    elif meme_url:
        await message.answer(text=meme_url)
    else:
        await message.answer(text=CONTENT_ERROR_TEXT)


# TODO: Добавить отправку чисто гифок и видео
