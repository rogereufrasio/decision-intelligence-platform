import asyncio
import logging
import time

import httpx

from src.core.config import get_settings
from src.infrastructure.http.exceptions import HttpClientException


logger = logging.getLogger(__name__)


class HttpClient:

    MAX_RETRIES = 3
    BACKOFF_SECONDS = 0.5

    def __init__(self):

        settings = get_settings()

        self.client = httpx.AsyncClient(
            timeout=settings.http_timeout_seconds,
        )

    async def _request(
        self,
        method: str,
        url: str,
        provider: str | None = None,
        **kwargs,
    ):

        last_exception = None

        started = time.perf_counter()

        for attempt in range(self.MAX_RETRIES):

            try:

                response = await getattr(
                    self.client,
                    method,
                )(
                    url,
                    **kwargs,
                )

                response.raise_for_status()

                elapsed = (
                    time.perf_counter() - started
                ) * 1000

                logger.info(
                    "provider=%s method=%s url=%s status=%s elapsed_ms=%.2f",
                    provider or "-",
                    method.upper(),
                    url,
                    response.status_code,
                    elapsed,
                )

                return response

            except (
                httpx.ConnectError,
                httpx.ReadTimeout,
                httpx.RemoteProtocolError,
                httpx.NetworkError,
            ) as exc:

                last_exception = exc

                logger.warning(
                    "provider=%s method=%s url=%s retry=%s error=%s",
                    provider or "-",
                    method.upper(),
                    url,
                    attempt + 1,
                    exc,
                )

                if attempt == self.MAX_RETRIES - 1:
                    break

                await asyncio.sleep(
                    self.BACKOFF_SECONDS * (2**attempt)
                )

            except httpx.HTTPError as exc:

                elapsed = (
                    time.perf_counter() - started
                ) * 1000

                logger.error(
                    "provider=%s method=%s url=%s elapsed_ms=%.2f error=%s",
                    provider or "-",
                    method.upper(),
                    url,
                    elapsed,
                    exc,
                )

                raise HttpClientException(
                    str(exc)
                ) from exc

        logger.error(
            "provider=%s method=%s url=%s retries_exhausted=%s error=%s",
            provider or "-",
            method.upper(),
            url,
            self.MAX_RETRIES,
            last_exception,
        )

        raise HttpClientException(
            str(last_exception)
        ) from last_exception

    async def get(
        self,
        url: str,
        provider: str | None = None,
        **kwargs,
    ):

        return await self._request(
            "get",
            url,
            provider=provider,
            **kwargs,
        )

    async def post(
        self,
        url: str,
        provider: str | None = None,
        **kwargs,
    ):

        return await self._request(
            "post",
            url,
            provider=provider,
            **kwargs,
        )

    async def close(self):
        if self.client.is_closed:
            return
        await self.client.aclose()
