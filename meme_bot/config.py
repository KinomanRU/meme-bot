from configparser import ConfigParser
from typing import Final

FILE: Final[str] = "settings.ini"
DEV_FILE: Final[str] = "settings_dev.ini"

FILES: Final[list[str]] = [
    FILE,
    "..\\" + FILE,
]
DEV_FILES: Final[list[str]] = [
    DEV_FILE,
    "..\\" + DEV_FILE,
]

config = ConfigParser()

if not config.read(DEV_FILES):
    if not config.read(FILES):
        raise FileNotFoundError
