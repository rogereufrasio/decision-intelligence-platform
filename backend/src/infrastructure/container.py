from src.infrastructure.http.client import HttpClient
from src.infrastructure.providers.provider_factory import ProviderFactory
from src.domain.travel.provider import TravelProvider


class Container:

    def __init__(self):

        self.http_client = HttpClient()

    def get_travel_provider(
        self,
        provider_name: str,
    ) -> TravelProvider:

        return ProviderFactory.create(
            provider_name=provider_name,
            client=self.http_client,
        )

    async def close(self):

        await self.http_client.close()