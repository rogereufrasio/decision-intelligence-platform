import pytest

from src.infrastructure.providers.amadeus_provider import AmadeusProvider
from src.shared.models import TravelSearchRequest


@pytest.mark.asyncio
async def test_amadeus_provider_requires_credentials():

    provider = AmadeusProvider()

    with pytest.raises(
        ValueError,
        match="Amadeus credentials are not configured",
    ):
        await provider.authenticate()


@pytest.mark.asyncio
async def test_amadeus_search_flight_offers(
    monkeypatch,
):

    provider = AmadeusProvider()

    async def fake_authenticate():
        return "fake-token"

    async def fake_get(
        path,
        **kwargs,
    ):
        assert path == "/v2/shopping/flight-offers"

        assert kwargs["headers"] == {
            "Authorization": "Bearer fake-token"
        }

        assert kwargs["params"] == {
            "originLocationCode": "GIG",
            "destinationLocationCode": "BRC",
            "departureDate": "2026-09-03",
            "adults": 2,
        }

        class Response:

            def json(self):
                return {
                    "data": [
                        {
                            "id": "1"
                        }
                    ]
                }

        return Response()

    monkeypatch.setattr(
        provider,
        "authenticate",
        fake_authenticate,
    )

    monkeypatch.setattr(
        provider,
        "get",
        fake_get,
    )

    request = TravelSearchRequest(
        origin="GIG",
        destination="BRC",
        departure_date="2026-09-03",
        adults=2,
    )

    result = await provider.search(request)

    assert result.provider == "amadeus"
    assert result.status == "success"
    assert "Offers found: 1" in result.message