import aiohttp
from config import PROXY, auth


async def request(url: str) -> tuple[int, str, str]:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=url,
            proxy=PROXY,
            proxy_auth=auth,
        ) as response:
            return response.status, response.reason, await response.text()
