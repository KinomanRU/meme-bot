__all__ = ("get_anecdote",)

import asyncio
import logging
from bs4 import BeautifulSoup
import log_utils
import request_utils
import strings
import urls

log = logging.getLogger(name=__name__)


def parse_html(text: str) -> str:
    if not text:
        return strings.CONTENT_ERROR
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
    return result or strings.CONTENT_ERROR


async def get_anecdote() -> str:
    resp_status: int
    resp_reason: str
    resp_text: str
    resp_status, resp_reason, resp_text = await request_utils.request(url=urls.ANECDOTE)
    result: str
    if resp_status == 200:
        result = parse_html(text=resp_text)
        log.debug("result=%r", result)
    else:
        result = str(resp_status) + " - " + resp_reason
    return result


async def main() -> None:
    log_utils.init_logging()
    await get_anecdote()


if __name__ == "__main__":
    asyncio.run(main())
