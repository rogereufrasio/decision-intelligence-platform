from src.domain.travel.provider import TravelProvider
from src.infrastructure.http.client import HttpClient
from src.infrastructure.providers.amadeus_auth_service import (
    AmadeusAuthService,
)
from src.infrastructure.providers.amadeus_provider import (
    AmadeusProvider,
)
from src.infrastructure.providers.mock_provider import (
    MockProvider,
)
from src.infrastructure.providers.provider_registry import (
    ProviderNotFoundError,
    ProviderRegistry,
)


class ProviderFactory:

    @classmethod
    def _bootstrap_defaults(cls) -> None:
        """Garante que os providers padrão estejam sempre cadastrados no Registry."""
        available = ProviderRegistry.list_available()

        def create_amadeus(client: HttpClient | None = None) -> TravelProvider:
            if client is None:
                client = HttpClient()
            return AmadeusProvider(
                client=client,
                auth_service=AmadeusAuthService(client=client),
            )

        def create_mock(client: HttpClient | None = None) -> TravelProvider:
            return MockProvider()

        if "amadeus" not in available:
            ProviderRegistry.register("amadeus", create_amadeus)
        if "mock" not in available:
            ProviderRegistry.register("mock", create_mock)

    @staticmethod
    def create(
        provider_name: str,
        client: HttpClient | None = None,
    ) -> TravelProvider:

        ProviderFactory._bootstrap_defaults()

        try:
            factory_fn = ProviderRegistry.get_factory(provider_name)
            return factory_fn(client)
        except ProviderNotFoundError:
            raise ValueError(
                f"Unsupported travel provider: {provider_name}"
            )