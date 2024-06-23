from os import getenv
from typing import Final
from aiohttp import BasicAuth
from aiogram.client.session.aiohttp import AiohttpSession

DEBUG_ENABLED: Final[bool] = True
PROXY_ENABLED: Final[bool] = False
BOT_TOKEN: Final[str] = getenv("BOT_TOKEN")
HELP_TEXT: Final[str] = (
    "Supported commands:\n/anec - random anecdote\n/meme - random meme"
)
CONTENT_ERROR_TEXT: Final[str] = "Sorry, but there is a problem with content"
ANECDOTE_URL: Final[str] = "https://www.anekdot.ru/random/anekdot/"
MEME_URL: Final[str] = "https://www.anekdot.ru/random/mem/"

# Proxy settings
PROXY: Final[str] = getenv("PROXY") if PROXY_ENABLED else None
auth = None
session = None
if PROXY_ENABLED:
    auth = BasicAuth(
        login=getenv("USERDOMAIN") + "\\" + getenv("USERNAME"),
        password=getenv("USERPASS"),
    )
    session = AiohttpSession(proxy=(PROXY, auth))