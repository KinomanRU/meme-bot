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
from request_utils import http_client
from tenacity import before_sleep_log, retry, stop_after_attempt

log = logging.getLogger(name=__name__)
router = Router(name=__name__)


@router.message(Command("anec"))
@retry(
    stop=stop_after_attempt(config.meme_search_attempts),
    before_sleep=before_sleep_log(log, logging.INFO),
)
async def handle_anecdote(message: Message) -> None:
    log_utils.log_command(log, logging.INFO, message)
    if message.bot:
        await message.bot.send_chat_action(
            chat_id=message.chat.id,
            action=ChatAction.TYPING,
        )
    anecdote_text: str = await get_anecdote(http_client)
    if anecdote_text:
        await message.answer(text=anecdote_text)
    else:
        await message.answer(text=strings.CONTENT_ERROR)


@router.message(Command("meme"))
@retry(
    stop=stop_after_attempt(config.meme_search_attempts),
    before_sleep=before_sleep_log(log, logging.INFO),
)
async def handle_meme(message: Message) -> None:
    log_utils.log_command(log, logging.INFO, message)
    if message.bot:
        await message.bot.send_chat_action(
            chat_id=message.chat.id,
            action=ChatAction.UPLOAD_DOCUMENT,
        )
    meme_url: str = await get_meme_link(http_client)
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
@retry(
    stop=stop_after_attempt(config.meme_search_attempts),
    before_sleep=before_sleep_log(log, logging.INFO),
)
async def handle_gmeme(message: Message) -> None:
    log_utils.log_command(log, logging.INFO, message)
    if message.bot:
        await message.bot.send_chat_action(
            chat_id=message.chat.id,
            action=ChatAction.UPLOAD_DOCUMENT,
        )
    meme_url: str = await get_meme_link(http_client, "gif")
    if meme_url.startswith("http"):
        await message.answer_animation(animation=meme_url)
    elif meme_url:
        await message.answer(text=meme_url)
    else:
        await message.answer(text=strings.CONTENT_ERROR)


@router.message(Command("vmeme"))
@retry(
    stop=stop_after_attempt(config.meme_search_attempts),
    before_sleep=before_sleep_log(log, logging.INFO),
)
async def handle_vmeme(message: Message) -> None:
    log_utils.log_command(log, logging.INFO, message)
    if message.bot:
        await message.bot.send_chat_action(
            chat_id=message.chat.id,
            action=ChatAction.UPLOAD_VIDEO,
        )
    meme_url: str = await get_meme_link(http_client, "video")
    if meme_url.startswith("http"):
        await message.answer_video(video=meme_url)
    elif meme_url:
        await message.answer(text=meme_url)
    else:
        await message.answer(text=strings.CONTENT_ERROR)
