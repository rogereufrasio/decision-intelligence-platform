from datetime import date, datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from src.application.ports import SearchRepository
from src.domain.entities.decision import SortCriterion
from src.domain.models import Offer, SearchCriteria, SearchSnapshot


def create_criteria() -> SearchCriteria:
    return SearchCriteria(
        origin="GIG",
        destination="GRU",
        departure_date=date(2026, 9, 3),
        return_date=date(2026, 9, 7),
        adults=2,
    )


def create_snapshot(search_id: str = "search-1") -> SearchSnapshot:
    return SearchSnapshot(
        search_id=search_id,
        criteria=create_criteria(),
        provider="mock",
        status="success",
        offers=[
            Offer(
                provider="mock",
                product_type="flight",
                price="150.00",
                currency="BRL",
            )
        ],
        sort_criterion=SortCriterion.CHEAPEST,
    )


def test_search_snapshot_uses_utc_and_independent_defaults() -> None:
    first = create_snapshot("search-1")
    second = create_snapshot("search-2")

    assert first.created_at.utcoffset() == timedelta(0)
    assert first.metadata == {}
    assert first.warnings == []
    assert first.metadata is not second.metadata
    assert first.warnings is not second.warnings


def test_search_snapshot_normalizes_created_at_to_utc() -> None:
    offset = timezone(timedelta(hours=-3))
    snapshot = SearchSnapshot(
        search_id="search-1",
        criteria=create_criteria(),
        created_at=datetime(2026, 9, 3, 10, 0, tzinfo=offset),
        provider="mock",
        status="success",
    )

    assert snapshot.created_at == datetime(
        2026,
        9,
        3,
        13,
        0,
        tzinfo=timezone.utc,
    )


def test_search_snapshot_rejects_naive_created_at() -> None:
    with pytest.raises(ValidationError):
        SearchSnapshot(
            search_id="search-1",
            criteria=create_criteria(),
            created_at=datetime(2026, 9, 3, 10, 0),
            provider="mock",
            status="success",
        )


def test_search_snapshot_is_immutable() -> None:
    snapshot = create_snapshot()

    with pytest.raises(ValidationError):
        snapshot.status = "error"


@pytest.mark.asyncio
async def test_search_repository_protocol_contract() -> None:
    class InMemorySearchRepository:
        def __init__(self) -> None:
            self.snapshots: dict[str, SearchSnapshot] = {}

        async def save(self, snapshot: SearchSnapshot) -> None:
            self.snapshots[snapshot.search_id] = snapshot

        async def get(self, search_id: str) -> SearchSnapshot | None:
            return self.snapshots.get(search_id)

        async def list_recent(
            self,
            limit: int = 20,
        ) -> list[SearchSnapshot]:
            return list(self.snapshots.values())[-limit:]

    repository: SearchRepository = InMemorySearchRepository()
    snapshot = create_snapshot()

    await repository.save(snapshot)

    assert await repository.get(snapshot.search_id) == snapshot
    assert await repository.list_recent() == [snapshot]
