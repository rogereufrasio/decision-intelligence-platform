from fastapi import APIRouter, Depends

from src.api.dependencies.travel import get_travel_service
from src.application.travel.travel_service import TravelService
from src.shared.models import (
    TravelOfferResponse,
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
    result = await service.search(request)

    return TravelSearchResponse(
        provider=result.provider,
        status=result.status,
        message=result.message,
        offers=[
            TravelOfferResponse(
                price=str(offer.price),
                currency=offer.currency,
            )
            for offer in result.offers
        ],
    )