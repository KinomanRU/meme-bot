__all__ = ("get_meme_link",)

import asyncio
import logging
from typing import Literal
from bs4 import BeautifulSoup
import log_utils
import request_utils
from config import config

log = logging.getLogger(name=__name__)


def search_any_meme(text: str) -> str:
    if not text:
        return ""
    bs: BeautifulSoup = BeautifulSoup(text, "html.parser")
    result: str = ""
    for i, topic in enumerate(bs.find_all(class_="topicbox")):
        # нулевой элемент - это заголовок
        if i == 0:
            continue
        # получаем тег, в котором указана ссылка на мем
        # картинка или гифка
        page_element = topic.find(name="img")
        if page_element is None or not page_element:
            # видео
            page_element = topic.find(name="source")
            if page_element is None or not page_element:
                continue
        result = str(page_element)
        # ищем ссылку
        result = result[result.find('src="') + 5 :]
        result = result[: result.find('"')]
        break
    return result


def search_gif_meme(text: str) -> str:
    if not text:
        return ""
    bs: BeautifulSoup = BeautifulSoup(text, "html.parser")
    result: str = ""
    for i, topic in enumerate(bs.find_all(class_="topicbox")):
        # нулевой элемент - это заголовок
        if i == 0:
            continue
        # получаем тег, в котором указана ссылка на гифку
        page_element = topic.find(name="img")
        if page_element is None or not page_element:
            continue
        result = str(page_element)
        # ищем ссылку
        result = result[result.find('src="') + 5 :]
        result = result[: result.find('"')]
        # если ссылка верная, то выходим из цикла, иначе ищем дальше на странице
        if result.split(".")[-1] == "gif":
            break
        else:
            result = ""
    return result


def search_video_meme(text: str) -> str:
    if not text:
        return ""
    bs: BeautifulSoup = BeautifulSoup(text, "html.parser")
    result: str = ""
    for i, topic in enumerate(bs.find_all(class_="topicbox")):
        # нулевой элемент - это заголовок
        if i == 0:
            continue
        # получаем тег, в котором указана ссылка на видео
        page_element = topic.find(name="source")
        if page_element is None or not page_element:
            continue
        result = str(page_element)
        # ищем ссылку
        result = result[result.find('src="') + 5 :]
        result = result[: result.find('"')]
        break
    return result


async def get_meme_link(what: Literal["gif", "video"] | None = None) -> str:
    if what not in ("gif", "video", None):
        log.debug(f"Incorrect parameter {what=}")
        return ""
    resp_status: int
    resp_reason: str
    resp_text: str
    result: str = ""
    attempts: int = config.getint("Bot", "Meme_Search_Attempts") if what else 1
    for _ in range(attempts):
        log.debug(f"iter={_}")
        resp_status, resp_reason, resp_text = await request_utils.request(
            url=config.get("Bot", "Meme_URL")
        )
        if resp_status == 200:
            match what:
                case None:
                    result = search_any_meme(text=resp_text)
                case "gif":
                    result = search_gif_meme(text=resp_text)
                case "video":
                    result = search_video_meme(text=resp_text)
            log.debug(f"{result=}")
            if result:
                break
        else:
            result = str(resp_status) + " - " + resp_reason
            break
    return result


async def main() -> None:
    log_utils.init_logging()
    choice = input("['gif', 'video', None]: ")
    await get_meme_link(choice if choice else None)


if __name__ == "__main__":
    asyncio.run(main())
