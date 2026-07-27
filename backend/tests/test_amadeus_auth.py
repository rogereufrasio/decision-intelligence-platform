import pytest

from src.core.config import get_settings
from src.infrastructure.providers.amadeus_provider import AmadeusProvider
from src.infrastructure.http.client import HttpClient


@pytest.mark.asyncio
async def test_amadeus_authentication_returns_token(
    monkeypatch,
):

    monkeypatch.setenv(
        "AMADEUS_CLIENT_ID",
        "test-client-id",
    )

    monkeypatch.setenv(
        "AMADEUS_CLIENT_SECRET",
        "test-client-secret",
    )


    get_settings.cache_clear()


    provider = AmadeusProvider(
        client=HttpClient()
    )


    class FakeResponse:

        def json(self):
            return {
                "access_token": "abc123",
                "expires_in": 1800,
            }


    async def fake_post(*args, **kwargs):

        return FakeResponse()


    monkeypatch.setattr(
        provider.client,
        "post",
        fake_post,
    )


    token = await provider.authenticate()


    assert token.access_token == "abc123"
    assert token.expires_in == 1800 
