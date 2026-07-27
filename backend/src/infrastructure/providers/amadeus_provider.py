from src.domain.travel.models import (
    TravelOffer,
    TravelResult,
)

from src.domain.travel.provider import TravelProvider
from src.domain.travel.auth import AccessToken

from src.core.config import get_settings

from src.shared.models import TravelSearchRequest

from src.infrastructure.providers.base_provider import (
    BaseProvider,
)

from src.infrastructure.http.client import (
    HttpClient,
)

from src.infrastructure.providers.amadeus_auth_service import (
    AmadeusAuthService,
)

from src.infrastructure.providers.amadeus_mapper import (
    AmadeusMapper,
)


class AmadeusProvider(
    BaseProvider,
    TravelProvider,
):

    def __init__(
        self,
        client: HttpClient,
        auth_service: AmadeusAuthService | None = None,
    ):

        settings = get_settings()

        super().__init__(
            client=client,
            base_url=settings.amadeus_base_url,
        )

        self.client_id = settings.amadeus_client_id
        self.client_secret = settings.amadeus_client_secret

        self.auth_service = auth_service or AmadeusAuthService(
            client=client,
        )

        self.mapper = AmadeusMapper()

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
            offers=[],
        )

    async def authenticate(self) -> AccessToken:

        if not self.client_id or not self.client_secret:
            raise ValueError(
                "Amadeus credentials are not configured"
            )

        return await self.auth_service.authenticate()

    def normalize_offers(
        self,
        data: dict,
    ) -> list[TravelOffer]:

        return self.mapper.normalize_offers(
            data
        )