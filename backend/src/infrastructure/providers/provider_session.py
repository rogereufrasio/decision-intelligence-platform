from abc import ABC
from typing import Any

from src.infrastructure.http.client import HttpClient


class ProviderSession(ABC):

    def __init__(
        self,
        client: HttpClient,
        base_url: str,
    ):
        self.client = client
        self.base_url = base_url

    @property
    def default_headers(
        self,
    ) -> dict[str, str]:

        return {
            "Accept": "application/json",
        }

    async def build_headers(
        self,
        **headers: str,
    ) -> dict[str, str]:

        merged = self.default_headers.copy()

        merged.update(
            {
                key: value
                for key, value in headers.items()
                if value is not None
            }
        )

        return merged

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