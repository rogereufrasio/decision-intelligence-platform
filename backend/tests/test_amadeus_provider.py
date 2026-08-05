import pytest
from unittest.mock import AsyncMock, Mock

from src.shared.models import TravelSearchRequest

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
async def test_amadeus_search_maps_request_and_canonical_offer():
    provider = create_provider()
    response = Mock()
    response.json.return_value = {
        "data": [{
            "price": {"grandTotal": "450.00", "currency": "BRL"}
        }]
    }
    provider.session.get = AsyncMock(return_value=response)
    request = TravelSearchRequest(
        origin="GIG", destination="GRU",
        departure_date="2026-10-01", return_date="2026-10-05", adults=2,
    )

    result = await provider.search(request)

    provider.session.get.assert_awaited_once_with(
        "/v2/shopping/flight-offers",
        params={
            "originLocationCode": "GIG",
            "destinationLocationCode": "GRU",
            "departureDate": "2026-10-01",
            "returnDate": "2026-10-05",
            "adults": 2,
        },
    )
    assert result.provider == "amadeus"
    assert str(result.offers[0].price) == "450.00"
    assert result.offers[0].currency == "BRL"


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
