from src.core.config import get_settings
from src.domain.travel.models import TravelOffer, TravelResult
from src.domain.travel.provider import TravelProvider
from src.infrastructure.providers.base_provider import BaseProvider
from src.shared.models import TravelSearchRequest


class AmadeusProvider(
    BaseProvider,
    TravelProvider,
):

    def __init__(self):

        settings = get_settings()

        self.client_id = settings.amadeus_client_id
        self.client_secret = settings.amadeus_client_secret

        super().__init__(
            base_url=settings.amadeus_base_url,
        )

    async def authenticate(self) -> str:

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
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )

        data = response.json()

        return data["access_token"]

    async def search_flight_offers(
        self,
        request: TravelSearchRequest,
        token: str,
    ) -> dict:

        response = await self.get(
            "/v2/shopping/flight-offers",
            params={
                "originLocationCode": request.origin,
                "destinationLocationCode": request.destination,
                "departureDate": request.departure_date,
                "adults": request.adults,
            },
            headers={
                "Authorization": f"Bearer {token}",
            },
        )

        return response.json()

    def normalize_offers(
        self,
        data: dict,
    ) -> list[TravelOffer]:

        offers = []

        for item in data.get("data", []):

            price = item.get(
                "price",
                {},
            )

            offers.append(
                TravelOffer(
                    price=price.get(
                        "grandTotal",
                        "0",
                    ),
                    currency=price.get(
                        "currency",
                        "UNKNOWN",
                    ),
                )
            )

        return offers

    async def search(
        self,
        request: TravelSearchRequest,
    ) -> TravelResult:

        token = await self.authenticate()

        data = await self.search_flight_offers(
            request,
            token,
        )

        offers = self.normalize_offers(data)

        return TravelResult(
            provider="amadeus",
            status="success",
            message=(
                f"Amadeus search completed: "
                f"{request.origin} -> {request.destination}"
            ),
            offers=offers,
        )