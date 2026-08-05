import logging

from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api.middleware.correlation_id import CorrelationIdMiddleware
from src.api.middleware.request_logging import RequestLoggingMiddleware
from src.core.metrics import MetricsCollector


def create_client(*, metrics_enabled: bool = True) -> tuple[TestClient, MetricsCollector]:
    app = FastAPI()
    collector = MetricsCollector()
    app.add_middleware(
        RequestLoggingMiddleware,
        metrics=collector,
        metrics_enabled=metrics_enabled,
    )
    app.add_middleware(CorrelationIdMiddleware)

    @app.get("/ok")
    async def ok() -> dict[str, bool]:
        return {"ok": True}

    @app.get("/error")
    async def error() -> None:
        raise RuntimeError("boom")

    return TestClient(app), collector


def test_logs_structured_request_fields(caplog) -> None:
    client, _ = create_client()
    with caplog.at_level(logging.INFO, logger="src.api.requests"):
        client.get("/ok", headers={"X-Correlation-ID": "log-id"})

    completed = next(
        record for record in caplog.records
        if record.message.startswith("request_completed")
    )
    assert completed.correlation_id == "log-id"
    assert completed.method == "GET"
    assert completed.path == "/ok"
    assert completed.status_code == 200
    assert completed.elapsed_ms >= 0


def test_error_has_header_is_logged_and_counted(caplog) -> None:
    client, collector = create_client()
    with caplog.at_level(logging.INFO, logger="src.api.requests"):
        response = client.get(
            "/error", headers={"X-Correlation-ID": "error-id"}
        )

    assert response.status_code == 500
    assert response.headers["X-Correlation-ID"] == "error-id"
    assert collector.snapshot()["total_errors"] == 1
    completed = next(
        record for record in caplog.records
        if record.message.startswith("request_completed")
    )
    assert completed.status_code == 500
    assert completed.elapsed_ms >= 0


def test_disabled_collection_does_not_break_requests() -> None:
    client, collector = create_client(metrics_enabled=False)
    assert client.get("/ok").status_code == 200
    assert collector.snapshot()["total_requests"] == 0
