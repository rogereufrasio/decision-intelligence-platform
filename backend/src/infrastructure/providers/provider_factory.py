from src.domain.travel.providers.base import TravelProvider
from src.infrastructure.providers.mock_provider import MockTravelProvider


def get_travel_provider() -> TravelProvider:
    """
    Centraliza a escolha do provider.

    Enquanto o MVP utiliza apenas Mock,
    futuras implementações (Amadeus, Duffel etc.)
    serão adicionadas aqui.
    """

    return MockTravelProvider()