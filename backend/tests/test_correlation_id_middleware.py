from uuid import UUID

from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.api.middleware.correlation_id import (
    CorrelationIdMiddleware,
    get_correlation_id,
)


def create_client() -> TestClient:
    app = FastAPI()
    app.add_middleware(CorrelationIdMiddleware)

    @app.get("/value")
    async def value() -> dict[str, str | None]:
        return {"correlation_id": get_correlation_id()}

    return TestClient(app)


def test_preserves_provided_correlation_id() -> None:
    response = create_client().get(
        "/value", headers={"X-Correlation-ID": "provided-id"}
    )
    assert response.headers["X-Correlation-ID"] == "provided-id"
    assert response.json()["correlation_id"] == "provided-id"


def test_generates_uuid4_and_returns_header() -> None:
    response = create_client().get("/value")
    generated = response.headers["X-Correlation-ID"]
    assert UUID(generated).version == 4
    assert response.json()["correlation_id"] == generated


def test_independent_requests_do_not_share_ids() -> None:
    client = create_client()
    first = client.get("/value").headers["X-Correlation-ID"]
    second = client.get("/value").headers["X-Correlation-ID"]
    assert first != second
