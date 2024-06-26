from configparser import ConfigParser
from typing import Final

FILES: Final[list[str]] = [
    "settings.ini",
    "..\\settings.ini",
]
DEV_FILES: Final[list[str]] = [
    "settings_dev.ini",
    "..\\settings_dev.ini",
]

config = ConfigParser()

if not config.read(DEV_FILES):
    if not config.read(FILES):
        raise FileExistsError
