import httpx

from src.core.config import get_settings


class HttpClient:

    def __init__(self):

        settings = get_settings()

        self.client = httpx.AsyncClient(
            timeout=settings.http_timeout_seconds,
        )

    async def close(self):

        await self.client.aclose()


http_client = HttpClient()