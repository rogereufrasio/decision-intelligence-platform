from datetime import date, datetime, timezone
from decimal import Decimal

import pytest

from src.application.travel.get_search_history import (
    GetSearchHistoryUseCase,
)
from src.application.travel.get_search_snapshot import (
    GetSearchSnapshotUseCase,
)
from src.domain.models import Offer, SearchCriteria, SearchSnapshot


def create_snapshot(search_id: str) -> SearchSnapshot:
    return SearchSnapshot(
        search_id=search_id,
        criteria=SearchCriteria(
            origin="GIG",
            destination="GRU",
            departure_date=date(2026, 9, 3),
            adults=1,
        ),
        created_at=datetime(2026, 8, 5, tzinfo=timezone.utc),
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
    )


class FakeSearchRepository:
    def __init__(self, snapshots: list[SearchSnapshot]) -> None:
        self.snapshots = snapshots
        self.requested_limit: int | None = None

    async def save(self, snapshot: SearchSnapshot) -> None:
        self.snapshots.append(snapshot)

    async def get(self, search_id: str) -> SearchSnapshot | None:
        return next(
            (
                snapshot
                for snapshot in self.snapshots
                if snapshot.search_id == search_id
            ),
            None,
        )

    async def list_recent(self, limit: int = 20) -> list[SearchSnapshot]:
        self.requested_limit = limit
        return self.snapshots[:limit]


@pytest.mark.asyncio
async def test_get_search_history_lists_recent_snapshots() -> None:
    snapshots = [create_snapshot("search-2"), create_snapshot("search-1")]
    repository = FakeSearchRepository(snapshots)
    use_case = GetSearchHistoryUseCase(repository)

    result = await use_case.execute(limit=2)

    assert result == snapshots
    assert repository.requested_limit == 2


@pytest.mark.asyncio
@pytest.mark.parametrize("limit", [0, 101])
async def test_get_search_history_rejects_invalid_limit(limit: int) -> None:
    use_case = GetSearchHistoryUseCase(FakeSearchRepository([]))

    with pytest.raises(ValueError, match="between 1 and 100"):
        await use_case.execute(limit)


@pytest.mark.asyncio
async def test_get_search_snapshot_returns_snapshot_by_id() -> None:
    snapshot = create_snapshot("search-1")
    use_case = GetSearchSnapshotUseCase(
        FakeSearchRepository([snapshot])
    )

    result = await use_case.execute("search-1")

    assert result is snapshot


@pytest.mark.asyncio
async def test_get_search_snapshot_returns_none_when_missing() -> None:
    use_case = GetSearchSnapshotUseCase(FakeSearchRepository([]))

    assert await use_case.execute("missing") is None
