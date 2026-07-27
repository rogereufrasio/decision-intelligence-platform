from src.domain.travel.models import TravelOffer, TravelResult
from src.domain.travel.provider import TravelProvider
from src.domain.travel.auth import AccessToken
from src.core.config import get_settings
from src.shared.models import TravelSearchRequest
from src.infrastructure.providers.base_provider import BaseProvider
from src.infrastructure.http.client import HttpClient
from src.infrastructure.providers.amadeus_mapper import AmadeusMapper


class AmadeusProvider(
    BaseProvider,
    TravelProvider,
):

    def __init__(
        self,
        client: HttpClient,
    ):

        settings = get_settings()

        super().__init__(
            client=client,
            base_url=settings.amadeus_base_url,
        )

        self.client_id = settings.amadeus_client_id
        self.client_secret = settings.amadeus_client_secret

        self.mapper = AmadeusMapper()

    async def search(
        self,
        request: TravelSearchRequest,
    ) -> TravelResult:

        token = await self.authenticate()

        response = await self.get(
            "/v2/shopping/flight-offers",
            params={
                "originLocationCode": request.origin,
                "destinationLocationCode": request.destination,
                "departureDate": request.departure_date,
                "returnDate": request.return_date,
                "adults": request.adults,
            },
            headers={
                "Authorization": (
                    f"Bearer {token.access_token}"
                ),
            },
        )

        offers = self.mapper.map_offers(
            response.json()
        )

        return TravelResult(
            provider="amadeus",
            status="success",
            message="Flight search completed",
            offers=offers,
        )

    async def authenticate(self) -> AccessToken:

        if not self.client_id or not self.client_secret:
            raise ValueError(
                "Amadeus credentials are not configured"
            )

        response = await self.post(
            "/v1/security/oauth2/token",
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
            headers={
                "Content-Type": (
                    "application/x-www-form-urlencoded"
                ),
            },
        )

        data = response.json()

        return AccessToken(
            access_token=data["access_token"],
            expires_in=data.get(
                "expires_in"
            ),
        )

    def normalize_offers(
        self,
        data: dict,
    ) -> list[TravelOffer]:

        return self.mapper.map_offers(data)