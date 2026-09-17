import logging

from aiogram.types import Message
from config import config


def log_command(logger: logging.Logger, level: int, message: Message) -> None:
    command: str = "Command '" + (message.text if message.text else "") + "'"
    logger.log(
        level,
        "%s from %r [%s]",
        command,
        message.from_user.full_name if message.from_user else "",
        message.from_user,
    )


def init_logging():
    logging.basicConfig(
        level=logging.DEBUG if config.debug else logging.INFO,
        format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
        filename=(config.log_file if config.log_to_file else None),
        encoding="utf-8",
    )
