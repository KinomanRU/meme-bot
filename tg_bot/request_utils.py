import aiohttp

import config as cfg


async def request(url: str) -> tuple[int, str, str]:
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url=url,
            proxy=cfg.PROXY,
            proxy_auth=cfg.auth,
        ) as response:
            return response.status, response.reason, await response.text()
