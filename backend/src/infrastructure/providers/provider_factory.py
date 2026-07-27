from src.domain.travel.provider import TravelProvider
from src.infrastructure.http.client import HttpClient
from src.infrastructure.providers.amadeus_provider import AmadeusProvider
from src.infrastructure.providers.mock_provider import MockTravelProvider


class ProviderFactory:

    @staticmethod
    def create(
        provider_name: str,
        client: HttpClient | None = None,
    ) -> TravelProvider:

        if provider_name == "mock":
            return MockTravelProvider()

        if provider_name == "amadeus":

            if client is None:
                client = HttpClient()

            return AmadeusProvider(
                client=client,
            )

        raise ValueError(
            f"Unsupported travel provider: {provider_name}"
        )