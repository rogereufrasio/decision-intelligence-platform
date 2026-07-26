from src.domain.travel.provider import TravelProvider
from src.domain.travel.models import TravelResult
from src.shared.models import TravelSearchRequest


class SearchTravelUseCase:

    def __init__(
        self,
        provider: TravelProvider,
    ):

        self.provider = provider

    async def execute(
        self,
        request: TravelSearchRequest,
    ) -> TravelResult:

        return await self.provider.search(request)