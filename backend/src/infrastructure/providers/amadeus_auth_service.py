from src.core.config import get_settings
from src.domain.travel.auth import AccessToken
from src.infrastructure.http.client import HttpClient


class AmadeusAuthService:

    def __init__(
        self,
        client: HttpClient,
        base_url: str = "https://test.api.amadeus.com",
    ):
        self.client = client
        self.base_url = base_url

    async def authenticate(
        self,
        client_id: str | None = None,
        client_secret: str | None = None,
    ) -> AccessToken:

        if not client_id or not client_secret:
            settings = get_settings()

            client_id = settings.amadeus_client_id
            client_secret = settings.amadeus_client_secret

        if not client_id or not client_secret:
            raise ValueError(
                "Amadeus credentials are not configured"
            )

        response = await self.client.post(
            f"{self.base_url}/v1/security/oauth2/token",
            data={
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret,
            },
        )

        data = response.json()

        return AccessToken(
            access_token=data["access_token"],
            expires_in=data.get(
                "expires_in"
            ),
        )