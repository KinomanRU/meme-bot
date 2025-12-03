import logging
from aiogram.types import Message
from config import config


def log_command(logger: logging.Logger, level: int, message: Message) -> None:
    command: str = "Command '" + (message.text if message.text else "") + "'"
    logger.log(
        level,
        "%s from %r [%s]",
        command,
        message.from_user.full_name,
        message.from_user,
    )


def init_logging():
    logging.basicConfig(
        level=logging.DEBUG if config.getboolean("Debug", "Debug") else logging.INFO,
        format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
        filename=(
            config.get("Logging", "Log_File")
            if config.getboolean("Logging", "Log_To_File")
            else None
        ),
        encoding="utf-8",
    )
