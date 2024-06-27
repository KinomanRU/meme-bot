import logging
from aiogram.types import Message
from config import config


def format_message(message: Message) -> str:
    command: str = (
        "Command '" + message.text + "'" if message.text else "No text command given"
    )
    return f"{command} from '{message.from_user.full_name}' [{str(message.from_user)}]"


def init_logging():
    logging.basicConfig(
        level=logging.DEBUG if config.getboolean("Debug", "Debug") else logging.INFO,
        format="{asctime} [{levelname}] [{name}] {message}",
        style="{",
        filename=(
            config.get("Logging", "Log_File")
            if config.getboolean("Logging", "Log_To_File")
            else None
        ),
        encoding="utf-8",
    )
