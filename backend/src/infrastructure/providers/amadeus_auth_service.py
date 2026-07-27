from src.domain.travel.auth import AccessToken
from src.domain.travel.auth_provider import AuthProvider
from src.core.config import get_settings
from src.infrastructure.http.client import HttpClient


class AmadeusAuthService(
    AuthProvider,
):

    def __init__(
        self,
        client: HttpClient,
    ):

        self.client = client

        settings = get_settings()

        self.client_id = settings.amadeus_client_id
        self.client_secret = settings.amadeus_client_secret

        self.base_url = settings.amadeus_base_url


    async def authenticate(self) -> AccessToken:

        if not self.client_id or not self.client_secret:
            raise ValueError(
                "Amadeus credentials are not configured"
            )

        response = await self.client.post(
            f"{self.base_url}/v1/security/oauth2/token",
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