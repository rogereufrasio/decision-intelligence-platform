from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

import duckdb
import pytest

from src.domain.entities.decision import SortCriterion
from src.domain.models import Offer, SearchCriteria, SearchSnapshot
from src.infrastructure.persistence import DuckDBSearchRepository


def create_snapshot(
    search_id: str,
    created_at: datetime,
    *,
    status: str = "success",
) -> SearchSnapshot:
    return SearchSnapshot(
        search_id=search_id,
        criteria=SearchCriteria(
            origin="GIG",
            destination="GRU",
            departure_date=date(2026, 9, 3),
            return_date=date(2026, 9, 7),
            adults=2,
        ),
        created_at=created_at,
        provider="mock",
        status=status,
        offers=[
            Offer(
                provider="mock",
                product_type="flight",
                price=Decimal("150.25"),
                currency="BRL",
                metadata={"fare_type": "standard"},
            )
        ],
        sort_criterion=SortCriterion.CHEAPEST,
        schema_version="1.0",
        correlation_id="correlation-1",
        metadata={"source": "test"},
        warnings=["test warning"],
    )


@pytest.mark.asyncio
async def test_creates_table_automatically(tmp_path: Path) -> None:
    database_path = tmp_path / "searches.duckdb"
    repository = DuckDBSearchRepository(database_path)

    assert await repository.list_recent() == []

    connection = duckdb.connect(str(database_path), read_only=True)
    try:
        tables = connection.execute("SHOW TABLES").fetchall()
    finally:
        connection.close()

    assert ("search_snapshots",) in tables


@pytest.mark.asyncio
async def test_save_and_get_preserve_snapshot_types(tmp_path: Path) -> None:
    repository = DuckDBSearchRepository(tmp_path / "searches.duckdb")
    created_at = datetime(2026, 9, 3, 13, 0, tzinfo=timezone.utc)
    snapshot = create_snapshot("search-1", created_at)

    await repository.save(snapshot)
    restored = await repository.get("search-1")

    assert restored == snapshot
    assert restored is not None
    assert restored.created_at.tzinfo is not None
    assert restored.created_at.utcoffset() == timedelta(0)
    assert restored.offers[0].price == Decimal("150.25")
    assert restored.sort_criterion is SortCriterion.CHEAPEST


@pytest.mark.asyncio
async def test_save_updates_existing_search_id(tmp_path: Path) -> None:
    repository = DuckDBSearchRepository(tmp_path / "searches.duckdb")
    created_at = datetime(2026, 9, 3, 13, 0, tzinfo=timezone.utc)

    await repository.save(create_snapshot("search-1", created_at))
    await repository.save(
        create_snapshot("search-1", created_at, status="updated")
    )

    restored = await repository.get("search-1")
    recent = await repository.list_recent()

    assert restored is not None
    assert restored.status == "updated"
    assert len(recent) == 1


@pytest.mark.asyncio
async def test_list_recent_orders_by_created_at_descending(
    tmp_path: Path,
) -> None:
    repository = DuckDBSearchRepository(tmp_path / "searches.duckdb")
    base_time = datetime(2026, 9, 3, 10, 0, tzinfo=timezone.utc)

    await repository.save(create_snapshot("oldest", base_time))
    await repository.save(
        create_snapshot("newest", base_time + timedelta(hours=2))
    )
    await repository.save(
        create_snapshot("middle", base_time + timedelta(hours=1))
    )

    snapshots = await repository.list_recent()

    assert [snapshot.search_id for snapshot in snapshots] == [
        "newest",
        "middle",
        "oldest",
    ]


@pytest.mark.asyncio
async def test_list_recent_applies_limit(tmp_path: Path) -> None:
    repository = DuckDBSearchRepository(tmp_path / "searches.duckdb")
    base_time = datetime(2026, 9, 3, 10, 0, tzinfo=timezone.utc)

    for index in range(3):
        await repository.save(
            create_snapshot(
                f"search-{index}",
                base_time + timedelta(hours=index),
            )
        )

    snapshots = await repository.list_recent(limit=2)

    assert [snapshot.search_id for snapshot in snapshots] == [
        "search-2",
        "search-1",
    ]


@pytest.mark.asyncio
async def test_repositories_use_isolated_databases(tmp_path: Path) -> None:
    first = DuckDBSearchRepository(tmp_path / "first.duckdb")
    second = DuckDBSearchRepository(tmp_path / "second.duckdb")
    created_at = datetime(2026, 9, 3, 13, 0, tzinfo=timezone.utc)

    await first.save(create_snapshot("search-1", created_at))

    assert await first.get("search-1") is not None
    assert await second.get("search-1") is None
