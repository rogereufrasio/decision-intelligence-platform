import pytest

from src.application.travel.analyze_price_history import AnalyzePriceHistoryUseCase
from src.domain.models import PriceTrend, SearchSnapshot
from src.domain.services import PriceIntelligenceEngine
from tests.test_price_intelligence_engine import create_snapshot


class FakeSearchRepository:
    def __init__(self, snapshots: list[SearchSnapshot]) -> None:
        self.snapshots = {snapshot.search_id: snapshot for snapshot in snapshots}

    async def save(self, snapshot: SearchSnapshot) -> None:
        self.snapshots[snapshot.search_id] = snapshot

    async def get(self, search_id: str) -> SearchSnapshot | None:
        return self.snapshots.get(search_id)

    async def list_recent(self, limit: int = 20) -> list[SearchSnapshot]:
        return list(self.snapshots.values())[:limit]


@pytest.mark.asyncio
async def test_analyzes_existing_search_history() -> None:
    snapshots = [
        create_snapshot("current", "90"),
        create_snapshot("previous", "100", days_ago=1),
    ]
    use_case = AnalyzePriceHistoryUseCase(
        FakeSearchRepository(snapshots), PriceIntelligenceEngine()
    )

    result = await use_case.execute("current")

    assert result is not None
    assert result.trend == PriceTrend.DECREASED


@pytest.mark.asyncio
async def test_returns_none_when_base_snapshot_does_not_exist() -> None:
    use_case = AnalyzePriceHistoryUseCase(
        FakeSearchRepository([]), PriceIntelligenceEngine()
    )

    assert await use_case.execute("missing") is None


@pytest.mark.asyncio
async def test_rejects_limit_outside_range() -> None:
    use_case = AnalyzePriceHistoryUseCase(
        FakeSearchRepository([]), PriceIntelligenceEngine()
    )

    with pytest.raises(ValueError, match="between 2 and 100"):
        await use_case.execute("search", limit=1)
