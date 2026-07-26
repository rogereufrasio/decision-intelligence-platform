from fastapi import APIRouter

from src.application.travel.search_travel_use_case import SearchTravelUseCase
from src.infrastructure.providers.mock_provider import MockTravelProvider
from src.shared.models import TravelSearchRequest, TravelSearchResponse

router = APIRouter(prefix="/travel", tags=["Travel"])


@router.post(
    "/search",
    response_model=TravelSearchResponse,
)
async def search(request: TravelSearchRequest):

    use_case = SearchTravelUseCase(
        provider=MockTravelProvider(),
    )

    return await use_case.execute(request)