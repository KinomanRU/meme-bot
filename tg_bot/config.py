import os
from typing import Final

from aiogram.client.session.aiohttp import AiohttpSession
from aiohttp import BasicAuth

DEBUG_ENABLED: Final[bool] = True
PROXY_ENABLED: Final[bool] = False
BOT_TOKEN: Final[str] = os.getenv("BOT_TOKEN")
HELP_TEXT: Final[str] = (
    "Supported commands:\n/anec - random anecdote\n/meme - random meme\n/gmeme - gif meme\n/vmeme - video meme"
)
CONTENT_ERROR_TEXT: Final[str] = "Sorry, but there is a problem with content"
INCORRECT_INPUT_TEXT: Final[str] = "Incorrect input. Type /help for help."
ANECDOTE_URL: Final[str] = "https://www.anekdot.ru/random/anekdot/"
MEME_URL: Final[str] = "https://www.anekdot.ru/random/mem/"
MEME_SEARCH_ATTEMPTS: Final[int] = 10

PROXY: Final[str] = os.getenv("PROXY") if PROXY_ENABLED else None
auth: BasicAuth = (
    BasicAuth(
        login=os.getenv("USERDOMAIN") + "\\" + os.getenv("USERNAME"),
        password=os.getenv("USERPASS"),
    )
    if PROXY_ENABLED
    else None
)
session: AiohttpSession = AiohttpSession(proxy=(PROXY, auth)) if PROXY_ENABLED else None
