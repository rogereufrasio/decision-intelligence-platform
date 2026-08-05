from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from src.api.v1.readiness import get_readiness_service
from src.core.config import Settings
from src.core.readiness import ReadinessService
from src.infrastructure.container import Container
from src.infrastructure.http.client import HttpClient
from src.main import app

client = TestClient(app)


def service(settings: Settings) -> tuple[ReadinessService, HttpClient]:
    http_client = HttpClient()
    return ReadinessService(settings, http_client), http_client


def test_readiness_returns_200_with_disabled_optional_adapters() -> None:
    readiness_service, http_client = service(Settings(
        ai_assistant_enabled=False,
        search_persistence_enabled=False,
        decision_persistence_enabled=False,
    ))
    app.dependency_overrides[get_readiness_service] = lambda: readiness_service
    try:
        response = client.get("/api/v1/readiness")
    finally:
        app.dependency_overrides.clear()
    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_invalid_external_configuration_returns_controlled_503() -> None:
    readiness_service, _ = service(Settings(
        external_dependency_check_enabled=True,
        travel_provider="amadeus",
        amadeus_client_id=None,
        amadeus_client_secret=None,
    ))
    app.dependency_overrides[get_readiness_service] = lambda: readiness_service
    try:
        response = client.get("/api/v1/readiness")
    finally:
        app.dependency_overrides.clear()
    assert response.status_code == 503
    body = response.json()
    assert body["status"] == "not_ready"
    assert "amadeus" not in response.text.lower()


def test_enabled_persistence_with_accessible_directory(tmp_path: Path) -> None:
    readiness_service, _ = service(Settings(
        search_persistence_enabled=True,
        search_database_path=str(tmp_path / "searches.duckdb"),
    ))
    assert readiness_service.evaluate().ready is True


def test_inaccessible_persistence_directory_is_controlled(
    tmp_path: Path,
) -> None:
    parent_file = tmp_path / "not-a-directory"
    parent_file.write_text("file", encoding="utf-8")
    readiness_service, _ = service(Settings(
        decision_persistence_enabled=True,
        decision_database_path=str(parent_file / "decisions.duckdb"),
    ))
    result = readiness_service.evaluate()
    assert result.ready is False
    check = next(
        item for item in result.checks
        if item.name == "decision_persistence"
    )
    assert check.message == "Persistence directory is unavailable."
    assert str(tmp_path) not in check.message


def test_external_configuration_accepts_minimum_credentials() -> None:
    readiness_service, _ = service(Settings(
        external_dependency_check_enabled=True,
        travel_provider="duffel",
        duffel_api_key="configured",
    ))
    assert readiness_service.evaluate().ready is True


@pytest.mark.asyncio
async def test_http_client_close_is_idempotent() -> None:
    http_client = HttpClient()
    await http_client.close()
    await http_client.close()
    assert http_client.client.is_closed


def test_container_exposes_readiness_without_creating_database(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "searches.duckdb"
    container = Container(Settings(
        search_persistence_enabled=True,
        search_database_path=str(database_path),
    ))
    assert isinstance(container.get_readiness_service(), ReadinessService)
    assert not database_path.exists()


def test_health_remains_available() -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
