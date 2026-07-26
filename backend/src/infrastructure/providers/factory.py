from src.domain.travel.provider import TravelProvider
from src.infrastructure.providers.mock_provider import MockTravelProvider


class ProviderFactory:

    @staticmethod
    def create() -> TravelProvider:
        return MockTravelProvider()