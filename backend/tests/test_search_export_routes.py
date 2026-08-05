from pathlib import Path

from fastapi.testclient import TestClient

from src.api.dependencies.travel import (
    get_export_search_snapshot_use_case,
)
from src.main import app


client = TestClient(app)


class FakeExportUseCase:
    def __init__(self, output_path: Path | None) -> None:
        self.output_path = output_path

    async def execute(self, search_id: str) -> Path | None:
        return self.output_path


def test_search_export_returns_file_response(tmp_path: Path) -> None:
    output_path = tmp_path / "search_search-1.parquet"
    output_path.write_bytes(b"PAR1testPAR1")
    app.dependency_overrides[
        get_export_search_snapshot_use_case
    ] = lambda: FakeExportUseCase(output_path)
    try:
        response = client.get(
            "/api/v1/search-history/search-1/export"
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.content == b"PAR1testPAR1"
    assert response.headers["content-type"] == (
        "application/vnd.apache.parquet"
    )
    assert "search_search-1.parquet" in response.headers[
        "content-disposition"
    ]


def test_search_export_returns_404_when_snapshot_is_missing() -> None:
    app.dependency_overrides[
        get_export_search_snapshot_use_case
    ] = lambda: FakeExportUseCase(None)
    try:
        response = client.get(
            "/api/v1/search-history/missing/export"
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404
    assert response.json()["detail"]["code"] == (
        "search_snapshot_not_found"
    )


def test_search_export_returns_503_when_persistence_disabled() -> None:
    app.dependency_overrides[
        get_export_search_snapshot_use_case
    ] = lambda: None
    try:
        response = client.get(
            "/api/v1/search-history/search-1/export"
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 503
    assert response.json()["detail"]["code"] == (
        "search_persistence_disabled"
    )


def test_search_export_rejects_path_traversal() -> None:
    app.dependency_overrides[
        get_export_search_snapshot_use_case
    ] = lambda: FakeExportUseCase(Path("unused"))
    try:
        response = client.get(
            "/api/v1/search-history/%2E%2E%5Csecret/export"
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "invalid_search_id"
