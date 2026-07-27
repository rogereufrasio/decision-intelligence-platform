import pytest

from src.infrastructure.providers.amadeus_auth_service import (
    AmadeusAuthService,
)
from src.infrastructure.http.client import HttpClient


@pytest.mark.asyncio
async def test_amadeus_auth_service_returns_token(
    monkeypatch,
):

    service = AmadeusAuthService(
        client=HttpClient()
    )


    class FakeResponse:

        def json(self):

            return {
                "access_token": "token123",
                "expires_in": 1800,
            }


    async def fake_post(*args, **kwargs):

        return FakeResponse()


    monkeypatch.setattr(
        service.client,
        "post",
        fake_post,
    )


    token = await service.authenticate()


    assert token.access_token == "token123"
    assert token.expires_in == 1800