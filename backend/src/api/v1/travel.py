from fastapi import APIRouter

from src.application.travel.travel_service import TravelService
from src.shared.models import (
    TravelSearchRequest,
    TravelSearchResponse,
)

router = APIRouter(
    prefix="/travel",
    tags=["Travel"],
)

service = TravelService()


@router.post(
    "/search",
    response_model=TravelSearchResponse,
)
async def search(
    request: TravelSearchRequest,
):
    return await service.search(request)