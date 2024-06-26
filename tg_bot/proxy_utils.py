from aiogram.client.session.aiohttp import AiohttpSession
from aiohttp import BasicAuth
from config import config
from typing import Final

PROXY: Final[bool] = config.getboolean("Proxy", "Proxy")
PROXY_URL: Final[str] = config.get("Proxy", "Proxy_URL") if PROXY else None
AUTH: Final[BasicAuth] = (
    BasicAuth(
        login=config.get("Proxy", "User_Name"),
        password=config.get("Proxy", "User_Pass"),
    )
    if PROXY
    else None
)
SESSION: Final[AiohttpSession] = (
    AiohttpSession(proxy=(PROXY_URL, AUTH)) if PROXY else None
)
