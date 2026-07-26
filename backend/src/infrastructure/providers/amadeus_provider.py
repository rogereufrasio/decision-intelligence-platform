from src.core.config import get_settings
from src.domain.travel.models import TravelResult
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