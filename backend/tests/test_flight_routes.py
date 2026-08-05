from unittest.mock import AsyncMock
import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.api.v1.flights import get_travel_service
from src.domain.travel.models import TravelResult, TravelOffer

client = TestClient(app)


def make_offer(offer_id: str) -> TravelOffer:
    return TravelOffer(
        id=offer_id,
        provider="mock",
        product_type="flight",
        price="150.00",
        currency="USD",
        cabin_class="economy",
        total_duration_minutes=120,
        slices=[],
    )


def test_search_flights_success():
    fake_service = AsyncMock()
    fake_service.search.return_value = TravelResult(
        provider="mock",
        status="success",
        message="Mocked search result",
        offers=[make_offer("1")],
    )

    app.dependency_overrides[get_travel_service] = lambda: fake_service
    try:
        response = client.post(
            "/api/v1/flights/search",
            json={
                "origin": "GIG",
                "destination": "GRU",
                "departure_date": "2026-09-03",
                "return_date": "2026-09-07",
                "passengers": 1,
                "sort_by": "best_value",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200

    body = response.json()

    assert body["total_results"] == 1
    assert body["applied_criterion"] == "best_value"
    assert isinstance(body["offers"], list)
    assert body["offers"][0]["id"] == "1"


def test_search_flights_empty():
    fake_service = AsyncMock()
    fake_service.search.return_value = TravelResult(
        provider="mock",
        status="success",
        message="No offers",
        offers=[],
    )

    app.dependency_overrides[get_travel_service] = lambda: fake_service
    try:
        response = client.post(
            "/api/v1/flights/search",
            json={
                "origin": "GIG",
                "destination": "GRU",
                "departure_date": "2026-09-03",
                "return_date": "2026-09-07",
                "passengers": 1,
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    body = response.json()
    assert body["total_results"] == 0
    assert body["offers"] == []


def test_search_flights_with_sorting():
    fake_service = AsyncMock()
    fake_service.search.return_value = TravelResult(
        provider="mock",
        status="success",
        message="Mocked sorted result",
        offers=[make_offer("1"), make_offer("2")],
    )

    app.dependency_overrides[get_travel_service] = lambda: fake_service
    try:
        response = client.post(
            "/api/v1/flights/search",
            json={
                "origin": "GIG",
                "destination": "GRU",
                "departure_date": "2026-09-03",
                "return_date": "2026-09-07",
                "passengers": 1,
                "sort_by": "best_value",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    body = response.json()
    assert body["total_results"] == 2