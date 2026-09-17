import logging

import aiohttp
import proxy_utils

log = logging.getLogger(name=__name__)


class HttpClient:
    def __init__(self):
        self._proxy_url = proxy_utils.PROXY_URL
        self._auth = proxy_utils.AUTH
        self._session: aiohttp.ClientSession | None = None

    async def _get_session(self) -> aiohttp.ClientSession:
        """Ленивая инициализация сессии (чтобы не создавать её вне event loop)"""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def request(self, url: str) -> tuple[int, str| None, str]:
        log.debug("request_url=%s", url)
        try:
            session = await self._get_session()
            async with session.get(
                url=url,
                proxy=self._proxy_url,
                proxy_auth=self._auth,
            ) as response:
                log.debug(
                    "response_status=%s response_reason=%s",
                    response.status,
                    response.reason,
                )
                return response.status, response.reason, await response.text()
        except Exception as err:
            log.exception("Error during request to %s: %s", url, str(err))
            return 400, "Bad Request", ""

    async def close(self):
        """Метод для корректного закрытия сессии при выходе из приложения"""
        if self._session and not self._session.closed:
            await self._session.close()


"""Singleton"""
http_client: HttpClient = HttpClient()
