import httpx

from src.core.config import get_settings
from src.infrastructure.http.exceptions import HttpClientException


class HttpClient:

    def __init__(self):

        settings = get_settings()

        self.client = httpx.AsyncClient(
            timeout=settings.http_timeout_seconds
        )

    async def get(
        self,
        url: str,
        **kwargs,
    ):

        try:

            response = await self.client.get(
                url,
                **kwargs,
            )

            response.raise_for_status()

            return response

        except httpx.HTTPError as exc:

            raise HttpClientException(
                str(exc)
            ) from exc


    async def post(
        self,
        url: str,
        **kwargs,
    ):

        try:

            response = await self.client.post(
                url,
                **kwargs,
            )

            response.raise_for_status()

            return response

        except httpx.HTTPError as exc:

            raise HttpClientException(
                str(exc)
            ) from exc