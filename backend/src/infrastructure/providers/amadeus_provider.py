from src.domain.travel.models import (
    TravelOffer,
    TravelResult,
)

from src.domain.travel.provider import TravelProvider
from src.domain.travel.auth import AccessToken
from src.domain.travel.auth_provider import AuthProvider

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
    AuthProvider,
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

        return await self.auth_service.authenticate()

    def normalize_offers(
        self,
        data: dict,
    ) -> list[TravelOffer]:

        return self.mapper.normalize_offers(
            data
        )