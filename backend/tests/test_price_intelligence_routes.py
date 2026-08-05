from datetime import date, datetime, timedelta, timezone
from decimal import Decimal

from fastapi.testclient import TestClient

from src.api.dependencies.travel import get_analyze_price_history_use_case
from src.application.travel.analyze_price_history import AnalyzePriceHistoryUseCase
from src.domain.models import Offer, SearchCriteria, SearchSnapshot
from src.domain.services import PriceIntelligenceEngine
from src.main import app


class FakeSearchRepository:
    def __init__(self, snapshots: list[SearchSnapshot]) -> None:
        self.snapshots = {snapshot.search_id: snapshot for snapshot in snapshots}

    async def save(self, snapshot: SearchSnapshot) -> None:
        self.snapshots[snapshot.search_id] = snapshot

    async def get(self, search_id: str) -> SearchSnapshot | None:
        return self.snapshots.get(search_id)

    async def list_recent(self, limit: int = 20) -> list[SearchSnapshot]:
        return list(self.snapshots.values())[:limit]


def snapshot(search_id: str, price: str, days_ago: int = 0) -> SearchSnapshot:
    return SearchSnapshot(
        search_id=search_id,
        criteria=SearchCriteria(
            origin="GIG",
            destination="GRU",
            departure_date=date(2026, 9, 3),
        ),
        created_at=datetime(2026, 8, 5, tzinfo=timezone.utc)
        - timedelta(days=days_ago),
        provider="aggregated",
        status="success",
        offers=[Offer(provider="mock", product_type="flight", price=Decimal(price), currency="BRL")],
    )


client = TestClient(app)


def test_route_returns_analysis_and_serializes_decimals() -> None:
    repository = FakeSearchRepository([
        snapshot("current", "90"), snapshot("previous", "100", 1)
    ])
    app.dependency_overrides[get_analyze_price_history_use_case] = lambda: (
        AnalyzePriceHistoryUseCase(repository, PriceIntelligenceEngine())
    )
    try:
        response = client.get("/api/v1/price-intelligence/current")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    body = response.json()
    assert body["current_price"] == "90"
    assert body["absolute_change"] == "-10"
    assert body["trend"] == "decreased"


def test_route_returns_404_for_missing_snapshot() -> None:
    use_case = AnalyzePriceHistoryUseCase(
        FakeSearchRepository([]), PriceIntelligenceEngine()
    )
    app.dependency_overrides[get_analyze_price_history_use_case] = lambda: use_case
    try:
        response = client.get("/api/v1/price-intelligence/missing")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404


def test_route_returns_503_when_persistence_is_disabled() -> None:
    app.dependency_overrides[get_analyze_price_history_use_case] = lambda: None
    try:
        response = client.get("/api/v1/price-intelligence/search")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 503


def test_route_returns_422_for_invalid_limit() -> None:
    use_case = AnalyzePriceHistoryUseCase(
        FakeSearchRepository([]), PriceIntelligenceEngine()
    )
    app.dependency_overrides[get_analyze_price_history_use_case] = lambda: use_case
    try:
        response = client.get("/api/v1/price-intelligence/search?limit=1")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 422
