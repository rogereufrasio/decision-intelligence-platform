from datetime import date, datetime, timezone
from decimal import Decimal

import pytest

from src.application.travel.compare_search_snapshots import (
    CompareSearchSnapshotsUseCase,
    NoComparableCurrencyError,
)
from src.domain.models import Offer, SearchCriteria, SearchSnapshot


def create_snapshot(
    search_id: str,
    offers: list[Offer],
) -> SearchSnapshot:
    return SearchSnapshot(
        search_id=search_id,
        criteria=SearchCriteria(
            origin="GIG",
            destination="GRU",
            departure_date=date(2026, 9, 3),
        ),
        created_at=datetime(2026, 8, 5, tzinfo=timezone.utc),
        provider="aggregated",
        status="success",
        offers=offers,
    )


def create_offer(provider: str, price: str, currency: str = "BRL") -> Offer:
    return Offer(
        provider=provider,
        product_type="flight",
        price=Decimal(price),
        currency=currency,
    )


class FakeSearchRepository:
    def __init__(self, snapshots: list[SearchSnapshot]) -> None:
        self.snapshots = {
            snapshot.search_id: snapshot for snapshot in snapshots
        }

    async def save(self, snapshot: SearchSnapshot) -> None:
        self.snapshots[snapshot.search_id] = snapshot

    async def get(self, search_id: str) -> SearchSnapshot | None:
        return self.snapshots.get(search_id)

    async def list_recent(self, limit: int = 20) -> list[SearchSnapshot]:
        return list(self.snapshots.values())[:limit]


@pytest.mark.asyncio
async def test_compare_snapshots_detects_price_reduction() -> None:
    base = create_snapshot("base", [create_offer("amadeus", "100.00")])
    target = create_snapshot("target", [create_offer("duffel", "80.00")])
    use_case = CompareSearchSnapshotsUseCase(
        FakeSearchRepository([base, target])
    )

    result = await use_case.execute("base", "target")

    assert result is not None
    assert result.base_lowest_price == Decimal("100.00")
    assert result.target_lowest_price == Decimal("80.00")
    assert result.absolute_price_difference == Decimal("20.00")
    assert result.percentage_price_difference == Decimal("-20.0")


@pytest.mark.asyncio
async def test_compare_snapshots_detects_price_increase() -> None:
    base = create_snapshot("base", [create_offer("amadeus", "80.00")])
    target = create_snapshot("target", [create_offer("amadeus", "100.00")])
    use_case = CompareSearchSnapshotsUseCase(
        FakeSearchRepository([base, target])
    )

    result = await use_case.execute("base", "target")

    assert result is not None
    assert result.absolute_price_difference == Decimal("20.00")
    assert result.percentage_price_difference == Decimal("25.00")


@pytest.mark.asyncio
async def test_compare_snapshots_uses_only_same_currency() -> None:
    base = create_snapshot(
        "base",
        [
            create_offer("amadeus", "100.00", "BRL"),
            create_offer("ignored", "1.00", "USD"),
        ],
    )
    target = create_snapshot(
        "target",
        [create_offer("duffel", "90.00", "BRL")],
    )
    use_case = CompareSearchSnapshotsUseCase(
        FakeSearchRepository([base, target])
    )

    result = await use_case.execute("base", "target")

    assert result is not None
    assert result.currency == "BRL"
    assert result.base_offer_count == 1
    assert result.target_offer_count == 1
    assert result.base_best_provider == "amadeus"
    assert result.target_best_provider == "duffel"


@pytest.mark.asyncio
async def test_compare_snapshots_rejects_incompatible_currencies() -> None:
    base = create_snapshot(
        "base",
        [create_offer("amadeus", "100.00", "BRL")],
    )
    target = create_snapshot(
        "target",
        [create_offer("duffel", "20.00", "USD")],
    )
    use_case = CompareSearchSnapshotsUseCase(
        FakeSearchRepository([base, target])
    )

    with pytest.raises(NoComparableCurrencyError):
        await use_case.execute("base", "target")


@pytest.mark.asyncio
async def test_compare_snapshots_returns_none_when_snapshot_missing() -> None:
    use_case = CompareSearchSnapshotsUseCase(FakeSearchRepository([]))

    assert await use_case.execute("base", "target") is None


@pytest.mark.asyncio
async def test_compare_snapshots_detects_provider_changes() -> None:
    base = create_snapshot(
        "base",
        [
            create_offer("amadeus", "100.00"),
            create_offer("legacy", "110.00"),
        ],
    )
    target = create_snapshot(
        "target",
        [
            create_offer("amadeus", "95.00"),
            create_offer("duffel", "90.00"),
        ],
    )
    use_case = CompareSearchSnapshotsUseCase(
        FakeSearchRepository([base, target])
    )

    result = await use_case.execute("base", "target")

    assert result is not None
    assert result.added_providers == ("duffel",)
    assert result.removed_providers == ("legacy",)
