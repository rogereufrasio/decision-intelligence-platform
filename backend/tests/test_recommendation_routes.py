from copy import deepcopy

from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


def create_offer(index: int) -> dict[str, object]:
    return {
        "provider": f"provider-{index}",
        "product_type": "flight",
        "price": str(100 + index),
        "currency": "BRL",
        "attributes": {"total_duration_minutes": 60 + index},
    }


def test_recommendations_returns_only_top_five() -> None:
    response = client.post(
        "/api/v1/recommendations",
        json={
            "offers": [create_offer(index) for index in range(7)],
            "profile": "balanced",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 5
    assert len(body["recommendations"]) == 5


def test_recommendations_returns_empty_result() -> None:
    response = client.post(
        "/api/v1/recommendations",
        json={"offers": [], "profile": "balanced"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "best_recommendation": None,
        "recommendations": [],
        "total": 0,
    }


def test_recommendations_rejects_invalid_profile() -> None:
    response = client.post(
        "/api/v1/recommendations",
        json={"offers": [], "profile": "unknown"},
    )

    assert response.status_code == 422
    assert response.json()["detail"]["code"] == (
        "invalid_preference_profile"
    )


def test_recommendations_serializes_decimals_and_best_item() -> None:
    response = client.post(
        "/api/v1/recommendations",
        json={
            "offers": [
                create_offer(1),
                create_offer(0),
            ],
            "profile": "cheapest",
        },
    )

    assert response.status_code == 200
    body = response.json()
    best = body["best_recommendation"]
    assert best == body["recommendations"][0]
    assert best["offer"]["price"] == "100"
    assert isinstance(best["score"]["overall_score"], str)
    assert set(best["score"]) == {
        "overall_score",
        "price_score",
        "duration_score",
        "provider_score",
    }
    assert isinstance(best["reasons"], list)


def test_recommendation_route_does_not_change_input_offers() -> None:
    offers = [create_offer(1), create_offer(0)]
    original = deepcopy(offers)

    response = client.post(
        "/api/v1/recommendations",
        json={"offers": offers, "profile": "fastest"},
    )

    assert response.status_code == 200
    assert offers == original
