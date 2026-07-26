from src.domain.travel.models import TravelResult
from src.shared.models import TravelSearchRequest


class SearchTravelUseCase:

    async def execute(
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
        )