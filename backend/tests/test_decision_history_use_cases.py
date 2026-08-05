from datetime import datetime, timezone
from uuid import UUID

import pytest

from src.application.travel.get_decision_history import GetDecisionHistoryUseCase
from src.application.travel.save_decision_snapshot import SaveDecisionSnapshotUseCase
from src.domain.models import (
    DecisionSnapshot,
    RecommendationEvaluation,
)
from tests.test_duckdb_decision_repository import create_snapshot


class FakeDecisionRepository:
    def __init__(self, snapshots: list[DecisionSnapshot] | None = None) -> None:
        self.snapshots = list(snapshots or [])

    async def save(self, snapshot: DecisionSnapshot) -> None:
        self.snapshots.append(snapshot)

    async def get(self, decision_id: str) -> DecisionSnapshot | None:
        return next((item for item in self.snapshots if item.decision_id == decision_id), None)

    async def list_recent(self, limit: int = 20) -> list[DecisionSnapshot]:
        return self.snapshots[:limit]


@pytest.mark.asyncio
async def test_save_generates_uuid_and_utc_timestamp() -> None:
    source = create_snapshot("source", datetime.now(timezone.utc))
    evaluation = RecommendationEvaluation(
        accepted=source.accepted,
        rejected=source.rejected,
        explanation=source.explanation,
    )
    repository = FakeDecisionRepository()

    result = await SaveDecisionSnapshotUseCase(repository).execute(
        evaluation, search_id="search-1"
    )

    assert UUID(result.decision_id).version == 4
    assert result.created_at.utcoffset() == timezone.utc.utcoffset(result.created_at)
    assert repository.snapshots == [result]


@pytest.mark.asyncio
async def test_history_uses_valid_limit() -> None:
    snapshots = [create_snapshot("one", datetime.now(timezone.utc))]
    repository = FakeDecisionRepository(snapshots)

    assert await GetDecisionHistoryUseCase(repository).execute(1) == snapshots


@pytest.mark.asyncio
@pytest.mark.parametrize("limit", [0, 101])
async def test_history_rejects_invalid_limits(limit: int) -> None:
    with pytest.raises(ValueError, match="between 1 and 100"):
        await GetDecisionHistoryUseCase(FakeDecisionRepository()).execute(limit)
