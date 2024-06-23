import logging
from config import DEBUG_ENABLED
from typing import Final
from aiogram import types
from typing import Literal

LOG_LEVEL: Final[int] = logging.DEBUG if DEBUG_ENABLED else logging.INFO
LOG_FORMAT: Final[str] = "{asctime} [{levelname}] [{name}] {message}"
LOG_STYLE: Final[Literal["{"]] = "{"
LOG_FILE: Final[str] = "tg_bot.log"
LOG_ENCODING: Final[str] = "utf-8"


def format_message(message: types.Message) -> str:
    command: str = (
        "Command '" + message.text + "'" if message.text else "No text command given"
    )
    return f"{command} from {message.from_user.full_name} [{str(message.from_user)}]"


def init_logging():
    logging.basicConfig(
        level=LOG_LEVEL,
        format=LOG_FORMAT,
        style=LOG_STYLE,
        filename=LOG_FILE if not DEBUG_ENABLED else None,
        encoding=LOG_ENCODING if not DEBUG_ENABLED else None,
    )
