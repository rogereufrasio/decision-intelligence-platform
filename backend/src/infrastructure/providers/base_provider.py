from typing import Any

from src.infrastructure.http.client import HttpClient


class BaseProvider:

    def __init__(
        self,
        client: HttpClient,
        base_url: str,
    ):

        self.client = client
        self.base_url = base_url.rstrip("/")

    async def get(
        self,
        path: str,
        **kwargs: Any,
    ):

        return await self.client.get(
            f"{self.base_url}{path}",
            **kwargs,
        )

    async def post(
        self,
        path: str,
        **kwargs: Any,
    ):

        return await self.client.post(
            f"{self.base_url}{path}",
            **kwargs,
        )