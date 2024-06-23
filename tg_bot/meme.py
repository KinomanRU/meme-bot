__all__ = ("get_meme_link",)

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
    return result or cfg.CONTENT_ERROR_TEXT


async def get_meme_link() -> str:
    resp_status: int
    resp_reason: str
    resp_text: str
    resp_status, resp_reason, resp_text = await request(url=cfg.MEME_URL)
    result: str
    if resp_status == 200:
        result = parse_text(text=resp_text)
    else:
        result = str(resp_status) + " - " + resp_reason
    return result


async def main() -> None:
    log_utils.init_logging()
    result: str = await get_meme_link()
    log.info(f"meme={result}")


if __name__ == "__main__":
    asyncio.run(main())
