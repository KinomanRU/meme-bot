__all__ = ("get_meme_link",)

import asyncio
import logging
from http import HTTPStatus

import log_utils
import urls
from bs4 import BeautifulSoup
from config import config
from request_utils import HttpClient, http_client

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


async def get_meme_link(
    http_client: HttpClient,
    what: str | None = None,
) -> str:
    if what not in ("gif", "video", None):
        log.debug("Incorrect parameter what=%r", what)
        return ""
    resp_status: int
    resp_reason: str | None
    resp_text: str
    result: str = ""
    attempts: int = config.meme_search_attempts if what else 1
    for _ in range(attempts):
        log.debug("iter=%s", _)
        resp_status, resp_reason, resp_text = await http_client.request(url=urls.MEME)
        if resp_status == HTTPStatus.OK:
            match what:
                case None:
                    result = search_any_meme(text=resp_text)
                case "gif":
                    result = search_gif_meme(text=resp_text)
                case "video":
                    result = search_video_meme(text=resp_text)
            log.debug("result=%r", result)
            if result:
                break
        else:
            result = str(resp_status) + " - " + str(resp_reason)
            break
    return result


async def main() -> None:
    log_utils.init_logging()
    choice = input("['gif', 'video', None]: ")
    await get_meme_link(http_client, choice if choice else None)
    await http_client.close()


if __name__ == "__main__":
    asyncio.run(main())
