from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_search_mock():

    response = client.post(
        "/api/v1/travel/search",
        json={
            "origin": "GIG",
            "destination": "BRC",
            "departure_date": "2026-09-03",
            "return_date": "2026-09-07",
            "adults": 2,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["provider"] == "mock"
    assert body["status"] == "success"
    assert body["message"] == "Travel search received: GIG -> BRC"