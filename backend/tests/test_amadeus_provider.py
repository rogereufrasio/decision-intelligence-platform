import pytest

from src.infrastructure.providers.amadeus_provider import (
    AmadeusProvider,
)
from src.infrastructure.providers.amadeus_auth_service import (
    AmadeusAuthService,
)
from src.infrastructure.http.client import HttpClient


def create_provider():

    client = HttpClient()

    return AmadeusProvider(
        client=client,
        auth_service=AmadeusAuthService(
            client=client,
        ),
    )


def test_normalize_amadeus_offers():

    provider = create_provider()

    data = {
        "data": [
            {
                "price": {
                    "grandTotal": "450.00",
                    "currency": "BRL",
                }
            }
        ]
    }

    offers = provider.normalize_offers(
        data
    )

    assert len(offers) == 1
    assert str(offers[0].price) == "450.00"
    assert offers[0].currency == "BRL"


@pytest.mark.asyncio
async def test_amadeus_provider_requires_credentials(
    monkeypatch,
):

    monkeypatch.delenv(
        "AMADEUS_CLIENT_ID",
        raising=False,
    )

    monkeypatch.delenv(
        "AMADEUS_CLIENT_SECRET",
        raising=False,
    )

    from src.core.config import get_settings

    get_settings.cache_clear()

    provider = create_provider()

    with pytest.raises(
        ValueError,
        match="Amadeus credentials are not configured",
    ):

        await provider.auth_service.authenticate()