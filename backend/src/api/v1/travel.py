from fastapi import APIRouter

from src.infrastructure.providers.mock_provider import MockTravelProvider
from src.application.travel.search_travel import SearchTravelUseCase
from src.shared.models import (
    TravelSearchRequest,
    TravelSearchResponse,
)

router = APIRouter(
    prefix="/travel",
    tags=["Travel"],
)

use_case = SearchTravelUseCase(
    provider=MockTravelProvider(),
)

@router.post(
    "/search",
    response_model=TravelSearchResponse,
)
async def search(
    request: TravelSearchRequest,
) -> TravelSearchResponse:

    result = await use_case.execute(request)

    return TravelSearchResponse(
        provider=result.provider,
        status=result.status,
        message=result.message,
    )