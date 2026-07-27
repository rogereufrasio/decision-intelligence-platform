from src.domain.travel.provider import TravelProvider

from src.infrastructure.http.client import HttpClient
from src.infrastructure.providers.amadeus_provider import (
    AmadeusProvider,
)
from src.infrastructure.providers.amadeus_auth_service import (
    AmadeusAuthService,
)
from src.infrastructure.providers.mock_provider import (
    MockProvider,
)


class ProviderFactory:

    @staticmethod
    def create(
        provider_name: str,
        client: HttpClient | None = None,
    ) -> TravelProvider:

        if client is None:
            client = HttpClient()

        match provider_name.lower():

            case "amadeus":

                return AmadeusProvider(
                    client=client,
                    auth_service=AmadeusAuthService(
                        client=client,
                    ),
                )

            case "mock":

                return MockProvider()

            case _:

                raise ValueError(
                    f"Unsupported travel provider: {provider_name}"
                )