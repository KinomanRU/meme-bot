from typing import Final

from aiogram.client.session.aiohttp import AiohttpSession
from aiohttp import BasicAuth
from config import config

PROXY: Final[bool] = config.proxy
PROXY_URL: Final[str] = config.proxy_url if PROXY else ""
AUTH: Final[BasicAuth] = (
    BasicAuth(
        login=config.user_name if PROXY else "",
        password=config.user_pass if PROXY else "",
    )
)
SESSION: Final[AiohttpSession] | None = (
    AiohttpSession(proxy=(PROXY_URL, AUTH)) if PROXY else None
)
