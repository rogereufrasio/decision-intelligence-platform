from src.domain.travel.models import TravelResult
from src.domain.travel.provider import TravelProvider
from src.shared.models import TravelSearchRequest


class AmadeusProvider(
      TravelProvider,
):

    async def search(
        self,
        request: TravelSearchRequest,
    ) -> TravelResult:

        return TravelResult(
            provider="amadeus",
            status="not_implemented",
            message=(
                f"Amadeus search pending: "
                f"{request.origin} -> {request.destination}"
            ),
        )