from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from src.domain.models import TravelResult
from src.infrastructure.container import Container
from src.main import app

client = TestClient(app)


@pytest.mark.parametrize("provider", ["mock", "amadeus", "duffel"])
def test_flight_search_selects_provider_from_header(
    monkeypatch: pytest.MonkeyPatch,
    provider: str,
) -> None:
    orchestrator = AsyncMock()
    orchestrator.search.return_value = TravelResult(
        provider=provider, status="success", message="OK", offers=[]
    )
    selected: list[str | None] = []

    def fake_orchestrator(
        self: Container,
        provider_name: str | None = None,
    ) -> AsyncMock:
        selected.append(provider_name)
        return orchestrator

    monkeypatch.setattr(Container, "get_search_orchestrator", fake_orchestrator)
    response = client.post(
        "/api/v1/flights/search",
        headers={"X-Travel-Provider": provider},
        json={
            "origin": "GIG", "destination": "GRU",
            "departure_date": "2026-09-03", "passengers": 1,
        },
    )
    assert response.status_code == 200
    assert selected == [provider]


def test_flight_search_rejects_unknown_provider() -> None:
    response = client.post(
        "/api/v1/flights/search",
        headers={"X-Travel-Provider": "unknown"},
        json={
            "origin": "GIG", "destination": "GRU",
            "departure_date": "2026-09-03", "passengers": 1,
        },
    )
    assert response.status_code == 400
    assert "X-Travel-Provider" in response.text
