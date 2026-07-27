from src.domain.travel.auth import AccessToken

from src.infrastructure.http.client import HttpClient


class AmadeusAuthService:

    def __init__(
        self,
        client: HttpClient,
    ):

        self.client = client

    async def authenticate(
        self,
    ) -> AccessToken:

        response = await self.client.post(
            "/v1/security/oauth2/token",
            data={
                "grant_type": "client_credentials",
            },
        )

        data = response.json()

        return AccessToken(
            access_token=data["access_token"],
            expires_in=data.get(
                "expires_in"
            ),
        )