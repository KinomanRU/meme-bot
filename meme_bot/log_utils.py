import logging
from logging.handlers import RotatingFileHandler

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
        stacklevel=2,
    )


def init_logging():
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] [%(name)s] %(message)s")
    if config.log_to_file:
        handler = RotatingFileHandler(
            filename=config.log_file,
            maxBytes=10 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8",
        )
    else:
        handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if config.debug else logging.INFO)
    logger.addHandler(handler)
