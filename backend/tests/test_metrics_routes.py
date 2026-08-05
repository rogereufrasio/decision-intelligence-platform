from fastapi.testclient import TestClient

from src.api.v1.metrics import get_metrics_collector
from src.core.config import Settings, get_settings
from src.core.metrics import MetricsCollector
from src.main import app

client = TestClient(app)


def test_metrics_count_and_group_requests() -> None:
    collector = MetricsCollector()
    collector.record(200, 10.0)
    collector.record(404, 20.0)
    collector.record(500, 30.0)
    app.dependency_overrides[get_metrics_collector] = lambda: collector
    try:
        response = client.get("/api/v1/metrics")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    body = response.json()
    assert body["total_requests"] == 3
    assert body["requests_by_status"] == {"200": 1, "404": 1, "500": 1}
    assert body["total_errors"] == 1
    assert body["average_response_time_ms"] == 20.0


def test_empty_metrics_have_non_negative_average() -> None:
    collector = MetricsCollector()
    app.dependency_overrides[get_metrics_collector] = lambda: collector
    try:
        response = client.get("/api/v1/metrics")
    finally:
        app.dependency_overrides.clear()
    assert response.json()["average_response_time_ms"] >= 0


def test_disabled_metrics_return_503() -> None:
    app.dependency_overrides[get_settings] = lambda: Settings(
        metrics_enabled=False
    )
    try:
        response = client.get("/api/v1/metrics")
    finally:
        app.dependency_overrides.clear()
    assert response.status_code == 503
