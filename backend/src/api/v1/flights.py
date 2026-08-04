from fastapi import APIRouter, Depends, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.api.schemas.flight_schema import (
    FlightSearchRequest,
    FlightSearchResponse,
)
from src.api.dependencies.travel import get_travel_service
from src.application.travel.travel_service import TravelService
from src.domain.entities.decision import SortCriterion
from src.domain.entities.flight import FlightOffer
from src.shared.exceptions import DIPException
from src.shared.models import TravelSearchRequest as SharedTravelSearchRequest


router = APIRouter(
    prefix="/flights",
    tags=["Flights"],
)


@router.post(
    "/search",
    response_model=FlightSearchResponse,
)
async def search_flights(
    request: FlightSearchRequest,
    service: TravelService = Depends(get_travel_service),
):
    shared_request = SharedTravelSearchRequest(
        origin=request.origin,
        destination=request.destination,
        departure_date=request.departure_date.isoformat(),
        return_date=request.return_date.isoformat() if request.return_date else None,
        adults=request.passengers,
    )

    try:
        result = await service.search(
            request=shared_request,
            criterion=request.sort_by,
        )
    except DIPException as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail={"code": exc.code, "message": exc.message},
        )
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail={
                "code": "service_unavailable",
                "message": "Travel providers are unavailable.",
            },
        )

    if result.status != "success":
        raise HTTPException(
            status_code=502,
            detail={
                "code": "provider_error",
                "message": result.message,
            },
        )

    flight_offers = [
        FlightOffer(
            id=str(index + 1),
            provider=result.provider,
            total_amount=offer.price,
            currency=offer.currency,
            total_duration_minutes=0,
            slices=[],
        )
        for index, offer in enumerate(result.offers)
    ]

    return FlightSearchResponse(
        total_results=len(flight_offers),
        applied_criterion=request.sort_by.value,
        offers=flight_offers,
    )


