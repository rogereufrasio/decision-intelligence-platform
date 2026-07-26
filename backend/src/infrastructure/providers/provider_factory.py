from src.domain.travel.provider import TravelProvider
from src.infrastructure.providers.amadeus_provider import AmadeusProvider
from src.infrastructure.providers.mock_provider import MockTravelProvider


class ProviderFactory:
    """
    Factory responsável pela criação dos providers de viagem.

    Novos providers (Amadeus, Duffel etc.)
    serão adicionados aqui futuramente.
    """

    @staticmethod
    def create(provider_name: str) -> TravelProvider:
        if provider_name == "mock":
            return MockTravelProvider()

        raise ValueError(
            f"Unsupported travel provider: {provider_name}"
        )