from src.core.config import get_settings
from src.domain.travel.auth import AccessToken
from src.domain.travel.provider import TravelProvider
from src.infrastructure.http.client import HttpClient
from src.infrastructure.providers.amadeus_auth_service import (
    AmadeusAuthService,
)
from src.infrastructure.providers.amadeus_mapper import (
    AmadeusMapper,
)
from src.infrastructure.providers.amadeus_session import (
    AmadeusSession,
)
from src.infrastructure.providers.base_provider import (
    BaseProvider,
)
from src.shared.models import (
    TravelSearchRequest,
    TravelSearchResponse,
)


class AmadeusProvider(
    TravelProvider,
):

    def __init__(
        self,
        client: HttpClient,
        auth_service: AmadeusAuthService | None = None,
    ):
    
        settings = get_settings()

        self.client_id = settings.amadeus_client_id
        self.client_secret = settings.amadeus_client_secret

        self.auth_service = auth_service or AmadeusAuthService(
            client=client,
        )

        self.session = AmadeusSession(
            client=client,
            auth_service=self.auth_service,
        )

    async def authenticate(
        self,
    ) -> AccessToken:

        return await self.auth_service.authenticate(
            self.client_id,
            self.client_secret,
        )

    def normalize_offers(
        self,
        data: dict,
    ):
        return AmadeusMapper.normalize_offers(
            data,
        )

    async def search(
        self,
        request: TravelSearchRequest,
    ) -> TravelSearchResponse:

        response = await self.session.get(
            "/v2/shopping/flight-offers",
            params={
                "originLocationCode": request.origin,
                "destinationLocationCode": request.destination,
                "departureDate": request.departure_date,
                "returnDate": request.return_date,
                "adults": request.adults,
            },
        )

        offers = self.normalize_offers(
            response.json(),
        )

        return TravelSearchResponse(
            provider="amadeus",
            status="success",
            message="Offers retrieved successfully",
            offers=offers,
        )