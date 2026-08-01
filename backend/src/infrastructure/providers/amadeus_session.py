from src.domain.travel.auth import AccessToken
from src.infrastructure.http.client import HttpClient
from src.infrastructure.providers.amadeus_auth_service import (
    AmadeusAuthService,
)
from src.infrastructure.providers.provider_session import (
    ProviderSession,
)


class AmadeusSession(ProviderSession):

    def __init__(
        self,
        client: HttpClient,
        auth_service: AmadeusAuthService,
        base_url: str = "https://test.api.amadeus.com",
    ):
        super().__init__(
            client=client,
            base_url=base_url,
        )

        self.auth_service = auth_service

    async def authenticate(
        self,
    ) -> AccessToken:

        return await self.auth_service.authenticate()

    @property
    async def headers(
        self,
    ) -> dict[str, str]:

        token = await self.authenticate()

        return await self.build_headers(
            Authorization=f"Bearer {token.access_token}",
        )

    async def get(
        self,
        path: str,
        **kwargs,
    ):

        kwargs["headers"] = await self.headers

        return await super().get(
            path,
            **kwargs,
        )

    async def post(
        self,
        path: str,
        **kwargs,
    ):

        kwargs["headers"] = await self.headers

        return await super().post(
            path,
            **kwargs,
        )