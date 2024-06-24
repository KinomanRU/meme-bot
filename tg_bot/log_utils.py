import logging
from typing import Final, Literal

from aiogram.types import Message

import config as cfg

LOG_LEVEL: Final[int] = logging.DEBUG if cfg.DEBUG_ENABLED else logging.INFO
LOG_FORMAT: Final[str] = "{asctime} [{levelname}] [{name}] {message}"
LOG_STYLE: Final[Literal["{"]] = "{"
LOG_FILE: Final[str] = "tg_bot.log"
LOG_ENCODING: Final[str] = "utf-8"


def format_message(message: Message) -> str:
    command: str = (
        "Command '" + message.text + "'" if message.text else "No text command given"
    )
    return f"{command} from {message.from_user.full_name} [{str(message.from_user)}]"


def init_logging():
    logging.basicConfig(
        level=LOG_LEVEL,
        format=LOG_FORMAT,
        style=LOG_STYLE,
        filename=LOG_FILE if not cfg.DEBUG_ENABLED else None,
        encoding=LOG_ENCODING if not cfg.DEBUG_ENABLED else None,
    )
