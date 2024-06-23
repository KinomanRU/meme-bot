__all__ = ("get_anecdote",)

import log_utils
import logging
import asyncio
from bs4 import BeautifulSoup
from request_utils import request
from config import CONTENT_ERROR_TEXT, ANECDOTE_URL

log = logging.getLogger(name=__name__)


def parse_html(text: str) -> str:
    if not text:
        return CONTENT_ERROR_TEXT
    bs: BeautifulSoup = BeautifulSoup(text, "html.parser")
    # получаем элемент, в котором написан текст анекдота
    result: str = str(bs.find_all(class_="topicbox")[1].find(class_="text"))
    # заменяем тег переноса на \n
    result = result.replace("<br />", "\n").replace("<br/>", "\n").replace("<br>", "\n")
    # удаляем лишние теги, которые попали в наш текст
    tmp_list: list = result.split(">")
    tmp_list[0] = ""
    result = "".join(tmp_list)
    tmp_list = result.split("<")
    tmp_list[-1] = ""
    result = "".join(tmp_list)
    return result or CONTENT_ERROR_TEXT


async def get_anecdote() -> str:
    resp_status: int
    resp_reason: str
    resp_text: str
    resp_status, resp_reason, resp_text = await request(url=ANECDOTE_URL)
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
