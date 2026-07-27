from src.application.travel.search_travel_use_case import SearchTravelUseCase
from src.core.config import get_settings
from src.infrastructure.container import Container
from src.domain.travel.provider import TravelProvider
from src.shared.models import TravelSearchRequest


class TravelService:

    def __init__(
        self,
        provider: TravelProvider | None = None,
    ):

        if provider is None:

            settings = get_settings()

            container = Container()

            provider = container.get_travel_provider(
                settings.travel_provider,
            )

        self.use_case = SearchTravelUseCase(
            provider
        )

    async def search(
        self,
        request: TravelSearchRequest,
    ):

        return await self.use_case.execute(request)