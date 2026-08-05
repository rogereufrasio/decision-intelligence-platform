from datetime import datetime, timezone
from pathlib import Path

from fastapi.testclient import TestClient

from src.api.dependencies.travel import get_decision_history_use_case
from src.application.travel.get_decision_history import GetDecisionHistoryUseCase
from src.core.config import Settings
from src.infrastructure.container import Container
from src.main import app
from tests.test_decision_history_use_cases import FakeDecisionRepository
from tests.test_duckdb_decision_repository import create_snapshot

client = TestClient(app)


def test_returns_503_when_persistence_disabled() -> None:
    app.dependency_overrides[get_decision_history_use_case] = lambda: None
    try:
        response = client.get("/api/v1/decision-history")
    finally:
        app.dependency_overrides.clear()
    assert response.status_code == 503


def test_returns_history_with_serialized_types() -> None:
    snapshot = create_snapshot(
        "decision-1", datetime(2026, 8, 5, 12, tzinfo=timezone.utc)
    )
    use_case = GetDecisionHistoryUseCase(FakeDecisionRepository([snapshot]))
    app.dependency_overrides[get_decision_history_use_case] = lambda: use_case
    try:
        response = client.get("/api/v1/decision-history")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 1
    assert body["items"][0]["selected_offer"]["price"] == "150.25"
    assert body["items"][0]["profile"] == "balanced"
    assert body["items"][0]["created_at"].endswith("Z")


def test_returns_empty_history() -> None:
    use_case = GetDecisionHistoryUseCase(FakeDecisionRepository())
    app.dependency_overrides[get_decision_history_use_case] = lambda: use_case
    try:
        response = client.get("/api/v1/decision-history")
    finally:
        app.dependency_overrides.clear()
    assert response.status_code == 200
    assert response.json() == {"items": [], "total": 0}


def test_rejects_invalid_limit() -> None:
    response = client.get("/api/v1/decision-history?limit=0")
    assert response.status_code == 422


def test_container_does_not_create_database_when_disabled(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "decisions.duckdb"
    container = Container(Settings(
        decision_persistence_enabled=False,
        decision_database_path=str(database_path),
    ))

    assert container.get_decision_repository() is None
    assert container.get_decision_history_use_case() is None
    assert not database_path.exists()
