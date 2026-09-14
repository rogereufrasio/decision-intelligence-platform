from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from src.api.dependencies.travel import get_travel_service
from src.domain.models import Offer, TravelResult
from src.main import app


def test_invalid_flight_payload_returns_serializable_400_response():
    response = TestClient(app, raise_server_exceptions=False).post(
        "/api/v1/flights/search",
        json={
            "origin": "12!",
            "destination": "GRU",
            "departure_date": "invalid",
            "passengers": 0,
        },
    )

    assert response.status_code == 400
    detail = response.json()["detail"]
    assert {tuple(error["loc"]) for error in detail} == {
        ("body", "origin"),
        ("body", "departure_date"),
        ("body", "passengers"),
    }


def test_flight_api_preserves_offer_duration():
    service = AsyncMock()
    service.search.return_value = TravelResult(
        provider="aggregate", status="success", message="ok",
        offers=[Offer(provider="mock", product_type="flight", price="450",
                      currency="BRL", attributes={"total_duration_minutes": 120,
                                                  "stops": 1})],
    )
    app.dependency_overrides[get_travel_service] = lambda: service
    try:
        response = TestClient(app).post("/api/v1/flights/search", json={
            "origin": "GIG", "destination": "GRU", "departure_date": "2027-01-10",
        })
    finally:
        app.dependency_overrides.clear()
    assert response.status_code == 200
    offer = response.json()["offers"][0]
    assert offer["total_duration_minutes"] == 120
