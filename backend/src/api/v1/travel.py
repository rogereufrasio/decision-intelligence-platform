from fastapi import APIRouter

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
) -> TravelSearchResponse:

    return TravelSearchResponse(
        provider="mock",
        status="success",
        message=(
            f"Travel search received: "
            f"{request.origin} -> {request.destination}"
        ),
    )