from datetime import date, datetime, timezone
from decimal import Decimal

from fastapi.testclient import TestClient

from src.api.dependencies.travel import (
    get_search_history_use_case,
    get_search_snapshot_use_case,
)
from src.domain.entities.decision import SortCriterion
from src.domain.models import Offer, SearchCriteria, SearchSnapshot
from src.main import app


client = TestClient(app)


def create_snapshot() -> SearchSnapshot:
    return SearchSnapshot(
        search_id="search-1",
        criteria=SearchCriteria(
            origin="GIG",
            destination="GRU",
            departure_date=date(2026, 9, 3),
            return_date=date(2026, 9, 7),
            adults=2,
        ),
        created_at=datetime(2026, 8, 5, 12, 30, tzinfo=timezone.utc),
        provider="mock",
        status="success",
        offers=[
            Offer(
                provider="mock",
                product_type="flight",
                price=Decimal("150.25"),
                currency="BRL",
            )
        ],
        sort_criterion=SortCriterion.CHEAPEST,
        schema_version="1.0",
    )


class FakeHistoryUseCase:
    async def execute(self, limit: int = 20) -> list[SearchSnapshot]:
        return [create_snapshot()][:limit]


class FakeSnapshotUseCase:
    def __init__(self, snapshot: SearchSnapshot | None) -> None:
        self.snapshot = snapshot

    async def execute(self, search_id: str) -> SearchSnapshot | None:
        return self.snapshot


def test_search_history_returns_503_when_persistence_disabled() -> None:
    app.dependency_overrides[get_search_history_use_case] = lambda: None
    try:
        response = client.get("/api/v1/search-history")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 503
    assert response.json()["detail"]["code"] == (
        "search_persistence_disabled"
    )


def test_search_history_returns_serialized_snapshots() -> None:
    app.dependency_overrides[get_search_history_use_case] = (
        FakeHistoryUseCase
    )
    try:
        response = client.get("/api/v1/search-history?limit=10")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert body["items"][0]["search_id"] == "search-1"
    assert body["items"][0]["offers"][0]["price"] == "150.25"
    assert body["items"][0]["created_at"] == (
        "2026-08-05T12:30:00Z"
    )
    assert body["items"][0]["sort_criterion"] == "cheapest"


def test_search_snapshot_returns_404_when_missing() -> None:
    app.dependency_overrides[get_search_snapshot_use_case] = lambda: (
        FakeSnapshotUseCase(None)
    )
    try:
        response = client.get("/api/v1/search-history/missing")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404
    assert response.json()["detail"]["code"] == (
        "search_snapshot_not_found"
    )
