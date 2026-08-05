from src.domain.travel.models import TravelOffer, TravelResult
from src.domain.travel.provider import TravelProvider
from src.shared.models import TravelSearchRequest


class MockTravelProvider(
    TravelProvider,
):

    async def search(
        self,
        request: TravelSearchRequest,
    ) -> TravelResult:

        return TravelResult(
            provider="mock",
            status="success",
            message=(
                f"Travel search received: "
                f"{request.origin} -> {request.destination}"
            ),
            offers=[
                TravelOffer(
                    provider="mock",
                    product_type="flight",
                    price="450.00",
                    currency="BRL",
                    attributes={
                        "total_duration_minutes": 120,
                        "stops": 0,
                    },
                )
            ],
        )


MockProvider = MockTravelProvider
