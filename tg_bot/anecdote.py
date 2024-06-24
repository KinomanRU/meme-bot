__all__ = ("get_anecdote",)

import asyncio
import logging

from bs4 import BeautifulSoup

import config as cfg
import log_utils
import request_utils

log = logging.getLogger(name=__name__)


def parse_html(text: str) -> str:
    if not text:
        return cfg.CONTENT_ERROR_TEXT
    bs: BeautifulSoup = BeautifulSoup(text, "html.parser")
    result: str = ""
    for i, topic in enumerate(bs.find_all(class_="topicbox")):
        # нулевой элемент - это заголовок
        if i == 0:
            continue
        # получаем элемент, в котором содержится текст анекдота
        page_element = topic.find(class_="text")
        if page_element is None or not page_element:
            continue
        result = str(page_element)
        # заменяем тег переноса на \n
        result = (
            result.replace("<br />", "\n").replace("<br/>", "\n").replace("<br>", "\n")
        )
        # удаляем лишние теги, которые попали в наш текст
        tmp_list: list = result.split(">")
        tmp_list[0] = ""
        result = "".join(tmp_list)
        tmp_list = result.split("<")
        tmp_list[-1] = ""
        result = "".join(tmp_list)
        break
    return result or cfg.CONTENT_ERROR_TEXT


async def get_anecdote() -> str:
    resp_status: int
    resp_reason: str
    resp_text: str
    resp_status, resp_reason, resp_text = await request_utils.request(
        url=cfg.ANECDOTE_URL
    )
    log.debug(f"{resp_status=} {resp_reason=}")
    result: str
    if resp_status == 200:
        result = parse_html(text=resp_text)
        log.debug(f"{result=}")
    else:
        result = str(resp_status) + " - " + resp_reason
    return result


async def main() -> None:
    log_utils.init_logging()
    await get_anecdote()


if __name__ == "__main__":
    asyncio.run(main())
