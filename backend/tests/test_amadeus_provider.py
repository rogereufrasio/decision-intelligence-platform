import pytest

from src.infrastructure.providers.amadeus_provider import AmadeusProvider
from src.infrastructure.http.client import HttpClient


def test_normalize_amadeus_offers():

    provider = AmadeusProvider(
        client=HttpClient()
    )

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

    offers = provider.normalize_offers(data)

    assert len(offers) == 1
    assert offers[0].price == "450.00"
    assert offers[0].currency == "BRL"


@pytest.mark.asyncio
async def test_amadeus_provider_requires_credentials():

    provider = AmadeusProvider(
        client=HttpClient()
    )

    with pytest.raises(
        ValueError,
        match="Amadeus credentials are not configured",
    ):
        await provider.authenticate()