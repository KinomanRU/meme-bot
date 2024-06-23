__all__ = ("get_anecdote",)

import config as cfg
import log_utils
import logging
import asyncio
from bs4 import BeautifulSoup
from request_utils import request

log = logging.getLogger(name=__name__)


def parse_text(text: str) -> str:
    if not text:
        return cfg.CONTENT_ERROR_TEXT
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
    return result or cfg.CONTENT_ERROR_TEXT


async def get_anecdote() -> str:
    resp_status: int
    resp_reason: str
    resp_text: str
    resp_status, resp_reason, resp_text = await request(url=cfg.ANECDOTE_URL)
    result: str
    if resp_status == 200:
        result = parse_text(text=resp_text)
    else:
        result = str(resp_status) + " - " + resp_reason
    return result


async def main() -> None:
    log_utils.init_logging()
    result: str = await get_anecdote()
    log.info(f"anecdote={result}")


if __name__ == "__main__":
    asyncio.run(main())
