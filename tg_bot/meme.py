__all__ = ("get_meme_link",)

import log_utils
import logging
import asyncio
from bs4 import BeautifulSoup
from request_utils import request
from config import MEME_URL, MEME_SEARCH_ATTEMPTS
from typing import Literal

log = logging.getLogger(name=__name__)


def search_any_meme(text: str) -> str:
    if not text:
        return ""
    bs: BeautifulSoup = BeautifulSoup(text, "html.parser")
    result: str
    # получаем тег, в котором указана ссылка на мем
    # картинка или гифка
    page_element = bs.find_all(class_="topicbox")[1].find(name="img")
    if page_element is None or not page_element:
        # видео
        page_element = bs.find_all(class_="topicbox")[1].find(name="source")
    result = str(page_element)
    # ищем ссылку
    result = result[result.find('src="') + 5 :]
    result = result[: result.find('"')]
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
    return result


async def get_meme_link(what: Literal["gif", "video"] | None = None) -> str:
    if what not in ("gif", "video", None):
        log.debug(f"Incorrect parameter {what=}")
        return ""
    resp_status: int
    resp_reason: str
    resp_text: str
    result: str = ""
    attempts: int = MEME_SEARCH_ATTEMPTS if what else 1
    for _ in range(attempts):
        log.debug(f"iter={_}")
        resp_status, resp_reason, resp_text = await request(url=MEME_URL)
        log.debug(f"{resp_status=} {resp_reason=}")
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
