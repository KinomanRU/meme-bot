import aiohttp
import proxy_utils
import logging

log = logging.getLogger(name=__name__)


async def request(url: str) -> tuple[int, str, str]:
    log.debug("request_url=%s", url)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=url,
                proxy=proxy_utils.PROXY_URL,
                proxy_auth=proxy_utils.AUTH,
            ) as response:
                log.debug(
                    "response_status=%s response_reason=%s",
                    response.status,
                    response.reason,
                )
                return response.status, response.reason, await response.text()
    except Exception as err:
        log.exception(str(err))
        return 400, "Bad Request", ""
