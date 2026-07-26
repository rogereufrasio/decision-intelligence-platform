from src.application.travel.search_travel_use_case import SearchTravelUseCase
from src.infrastructure.providers.provider_factory import ProviderFactory
from src.shared.models import TravelSearchRequest


class TravelService:
    def __init__(self):
        provider = ProviderFactory.create("mock")
        self.use_case = SearchTravelUseCase(provider)

    async def search(self, request: TravelSearchRequest):
        return await self.use_case.execute(request)