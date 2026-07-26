from fastapi import APIRouter, Depends

from src.api.dependencies.travel import get_travel_service
from src.application.travel.travel_service import TravelService
from src.shared.models import (
    TravelSearchRequest,
    TravelSearchResponse,
)


router = APIRouter(
    prefix="/travel",
    tags=["Travel"],
)


@router.post(
    "/search",
    response_model=TravelSearchResponse,
)
async def search(
    request: TravelSearchRequest,
    service: TravelService = Depends(
        get_travel_service
    ),
):
    return await service.search(request)