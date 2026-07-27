from src.domain.travel.models import TravelResult
from src.domain.travel.auth import AccessToken
from src.domain.travel.provider import TravelProvider
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

        self.client = client
        self.mapper = AmadeusMapper()

        settings = get_settings()

        self.client_id = settings.amadeus_client_id
        self.client_secret = settings.amadeus_client_secret

        super().__init__(
            client=client,
            base_url=settings.amadeus_base_url,
        )

    async def search(
        self,
        request: TravelSearchRequest,
    ) -> TravelResult:

        token = await self.authenticate()

        response = await self.client.get(
            "/v2/shopping/flight-offers",
            headers={
                "Authorization": (
                    f"Bearer {token.access_token}"
                ),
            },
            params={
                "originLocationCode": request.origin,
                "destinationLocationCode": request.destination,
                "departureDate": request.departure_date,
                "adults": request.adults,
            },
        )

        offers = self.mapper.normalize_offers(
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

        response = await self.client.post(
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