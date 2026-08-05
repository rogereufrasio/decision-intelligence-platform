from decimal import Decimal

import httpx
import pytest

from src.core.config import get_settings
from src.infrastructure.http.client import HttpClient
from src.infrastructure.providers.duffel_provider import DuffelProvider
from src.infrastructure.providers.duffel_provider import TravelResult
from src.shared.models import TravelSearchRequest


@pytest.fixture(autouse=True)
def clear_settings():
    get_settings.cache_clear()


def create_provider():
    client = HttpClient()
    return DuffelProvider(
        client=client,
    )


@pytest.mark.asyncio
async def test_duffel_provider_search_success(monkeypatch):
    monkeypatch.setenv("DUFFEL_API_KEY", "test-duffel-key")
    get_settings.cache_clear()

    provider = create_provider()

    class FakeResponse:
        def __init__(self, payload, status_code=200):
            self._payload = payload
            self.status_code = status_code

        def raise_for_status(self):
            return None

        def json(self):
            return self._payload

    captured = {}

    async def fake_post(*args, **kwargs):
        captured.update(kwargs)
        return FakeResponse(
            {
                "data": [
                    {
                        "offers": [
                            {
                                "total_amount": "300.00",
                                "total_currency": "BRL",
                            }
                        ]
                    }
                ]
            }
        )

    monkeypatch.setattr(
        provider.client.client,
        "post",
        fake_post,
    )

    request = TravelSearchRequest(
        origin="GIG",
        destination="GRU",
        departure_date="2026-10-01",
        adults=1,
    )

    result = await provider.search(request)

    assert result.provider == "duffel"
    assert result.status == "success"
    assert result.message == "Offers retrieved successfully"
    assert len(result.offers) == 1
    assert result.offers[0].price == Decimal("300.00")
    assert result.offers[0].currency == "BRL"
    assert captured["json"] == {
        "slices": [{
            "origin": "GIG",
            "destination": "GRU",
            "departure_date": "2026-10-01",
        }],
        "passengers": [{"type": "adult"}],
    }
    assert captured["headers"]["Authorization"] == (
        "Bearer test-duffel-key"
    )


@pytest.mark.asyncio
async def test_duffel_provider_search_http_error(monkeypatch):
    monkeypatch.setenv("DUFFEL_API_KEY", "test-duffel-key")
    get_settings.cache_clear()

    provider = create_provider()

    async def fake_post(*args, **kwargs):
        raise httpx.HTTPStatusError(
            "Unauthorized",
            request=httpx.Request("POST", "https://api.duffel.com/air/offer_requests"),
            response=httpx.Response(401),
        )

    monkeypatch.setattr(
        provider.client.client,
        "post",
        fake_post,
    )

    request = TravelSearchRequest(
        origin="GIG",
        destination="GRU",
        departure_date="2026-10-01",
        adults=1,
    )

    result = await provider.search(request)

    assert result.provider == "duffel"
    assert result.status == "error"
    assert "Duffel search failed" in result.message
    assert result.offers == []
