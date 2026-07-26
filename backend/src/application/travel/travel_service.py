from src.application.travel.search_travel_use_case import SearchTravelUseCase
from src.application.dependencies.travel_dependencies import (
    get_travel_provider,
)
from src.shared.models import TravelSearchRequest


class TravelService:

    def __init__(self):

        provider = get_travel_provider()

        self.use_case = SearchTravelUseCase(
            provider
        )

    async def search(
        self,
        request: TravelSearchRequest,
    ):

        return await self.use_case.execute(request)