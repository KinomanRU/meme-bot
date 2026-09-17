from configparser import ConfigParser
from typing import Final

from pydantic_settings import BaseSettings, SettingsConfigDict

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

config_file = ConfigParser()

if not config_file.read(DEV_FILES) and not config_file.read(FILES):
    raise FileNotFoundError


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=".env",
    )
    debug: bool = config_file.getboolean("Debug", "Debug")
    bot_token: str = ""
    meme_search_attempts: int = config_file.getint("Bot", "Meme_Search_Attempts")
    log_to_file: bool = config_file.getboolean("Logging", "Log_To_File")
    log_file: str = config_file.get("Logging", "Log_File")
    proxy: bool = config_file.getboolean("Proxy", "Proxy")
    proxy_url: str = config_file.get("Proxy", "Proxy_URL")
    user_name: str = config_file.get("Proxy", "User_Name")
    user_pass: str = config_file.get("Proxy", "User_Pass")


config: Settings = Settings()
