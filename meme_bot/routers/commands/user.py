import logging

import log_utils
import strings
from aiogram import Router
from aiogram.enums import ChatAction
from aiogram.filters import Command
from aiogram.types import Message
from anecdote import get_anecdote
from config import config
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
    anecdote_text: str
    for i in range(config.getint("Bot", "Meme_Search_Attempts")):
        try:
            anecdote_text = await get_anecdote()
            if anecdote_text:
                await message.answer(text=anecdote_text)
            else:
                await message.answer(text=strings.CONTENT_ERROR)
            break
        except Exception as e:
            log.error(str(e))
            log.error(f"Attempt {i + 1} failed, retrying...")
    else:
        log.warning("All attempts failed")


@router.message(Command("meme"))
async def handle_meme(message: Message) -> None:
    log_utils.log_command(log, logging.INFO, message)
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_DOCUMENT,
    )
    meme_url: str
    for i in range(config.getint("Bot", "Meme_Search_Attempts")):
        try:
            meme_url = await get_meme_link()
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
            break
        except Exception as e:
            log.error(str(e))
            log.error(f"Attempt {i + 1} failed, retrying...")
    else:
        log.warning("All attempts failed")


@router.message(Command("gmeme"))
async def handle_gmeme(message: Message) -> None:
    log_utils.log_command(log, logging.INFO, message)
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_DOCUMENT,
    )
    meme_url: str
    for i in range(config.getint("Bot", "Meme_Search_Attempts")):
        try:
            meme_url = await get_meme_link("gif")
            if meme_url.startswith("http"):
                await message.answer_animation(animation=meme_url)
            elif meme_url:
                await message.answer(text=meme_url)
            else:
                await message.answer(text=strings.CONTENT_ERROR)
            break
        except Exception as e:
            log.error(str(e))
            log.error(f"Attempt {i + 1} failed, retrying...")
    else:
        log.warning("All attempts failed")


@router.message(Command("vmeme"))
async def handle_vmeme(message: Message) -> None:
    log_utils.log_command(log, logging.INFO, message)
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_VIDEO,
    )
    meme_url: str
    for i in range(config.getint("Bot", "Meme_Search_Attempts")):
        try:
            meme_url = await get_meme_link("video")
            if meme_url.startswith("http"):
                await message.answer_video(video=meme_url)
            elif meme_url:
                await message.answer(text=meme_url)
            else:
                await message.answer(text=strings.CONTENT_ERROR)
            break
        except Exception as e:
            log.error(str(e))
            log.error(f"Attempt {i + 1} failed, retrying...")
    else:
        log.warning("All attempts failed")
