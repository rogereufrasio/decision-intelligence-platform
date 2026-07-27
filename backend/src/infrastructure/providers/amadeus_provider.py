from src.domain.travel.models import TravelOffer, TravelResult
from src.domain.travel.auth import AccessToken
from src.domain.travel.provider import TravelProvider
from src.core.config import get_settings
from src.shared.models import TravelSearchRequest
from src.infrastructure.providers.base_provider import BaseProvider
from src.infrastructure.http.client import HttpClient


class AmadeusProvider(
    BaseProvider,
    TravelProvider,
):

    def __init__(
        self,
        client: HttpClient,
    ):

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

        return TravelResult(
            provider="amadeus",
            status="not_implemented",
            message=(
                f"Amadeus search pending: "
                f"{request.origin} -> {request.destination}"
            ),
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
                        "0.00",
                    ),
                    currency=price.get(
                        "currency",
                        "BRL",
                    ),
                )
            )

        return offers