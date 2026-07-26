from typing import Any

import httpx


class BaseProvider:

    def __init__(
        self,
        base_url: str,
        timeout: int = 30,
    ):

        self.base_url = base_url.rstrip("/")

        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=timeout,
        )

    async def get(
        self,
        path: str,
        **kwargs: Any,
    ):

        response = await self.client.get(
            path,
            **kwargs,
        )

        response.raise_for_status()

        return response

    async def post(
        self,
        path: str,
        **kwargs: Any,
    ):

        response = await self.client.post(
            path,
            **kwargs,
        )

        response.raise_for_status()

        return response

    async def close(self):

        await self.client.aclose()