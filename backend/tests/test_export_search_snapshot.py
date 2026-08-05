from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path

import duckdb
import pytest

from src.application.travel.export_search_snapshot import (
    ExportSearchSnapshotUseCase,
)
from src.domain.models import Offer, SearchCriteria, SearchSnapshot


def create_snapshot(search_id: str = "search-1") -> SearchSnapshot:
    return SearchSnapshot(
        search_id=search_id,
        criteria=SearchCriteria(
            origin="GIG",
            destination="GRU",
            departure_date=date(2026, 9, 3),
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
    )


class FakeSearchRepository:
    def __init__(self, snapshot: SearchSnapshot | None) -> None:
        self.snapshot = snapshot

    async def save(self, snapshot: SearchSnapshot) -> None:
        self.snapshot = snapshot

    async def get(self, search_id: str) -> SearchSnapshot | None:
        if self.snapshot is None or self.snapshot.search_id != search_id:
            return None
        return self.snapshot

    async def list_recent(self, limit: int = 20) -> list[SearchSnapshot]:
        return [self.snapshot] if self.snapshot is not None else []


@pytest.mark.asyncio
async def test_exports_snapshot_to_parquet(tmp_path: Path) -> None:
    snapshot = create_snapshot()
    export_directory = tmp_path / "exports"
    use_case = ExportSearchSnapshotUseCase(
        repository=FakeSearchRepository(snapshot),
        export_directory=export_directory,
    )

    output_path = await use_case.execute(snapshot.search_id)

    assert output_path == export_directory / "search_search-1.parquet"
    assert output_path is not None
    assert output_path.is_file()


@pytest.mark.asyncio
async def test_creates_missing_export_directory(tmp_path: Path) -> None:
    snapshot = create_snapshot()
    export_directory = tmp_path / "missing" / "exports"
    use_case = ExportSearchSnapshotUseCase(
        repository=FakeSearchRepository(snapshot),
        export_directory=export_directory,
    )

    await use_case.execute(snapshot.search_id)

    assert export_directory.is_dir()


@pytest.mark.asyncio
async def test_returns_none_when_snapshot_is_missing(tmp_path: Path) -> None:
    use_case = ExportSearchSnapshotUseCase(
        repository=FakeSearchRepository(None),
        export_directory=tmp_path,
    )

    assert await use_case.execute("missing") is None


@pytest.mark.asyncio
async def test_exports_valid_parquet_file(tmp_path: Path) -> None:
    snapshot = create_snapshot()
    use_case = ExportSearchSnapshotUseCase(
        repository=FakeSearchRepository(snapshot),
        export_directory=tmp_path,
    )

    output_path = await use_case.execute(snapshot.search_id)

    assert output_path is not None
    connection = duckdb.connect(":memory:")
    try:
        row = connection.execute(
            "SELECT search_id, offers_json FROM read_parquet(?)",
            [str(output_path)],
        ).fetchone()
    finally:
        connection.close()

    assert row is not None
    assert row[0] == snapshot.search_id
    assert '"price":"150.25"' in row[1]
