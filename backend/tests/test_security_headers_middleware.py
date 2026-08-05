from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from src.api.middleware.security_headers import SecurityHeadersMiddleware


def create_client(enabled: bool = True) -> TestClient:
    app = FastAPI()
    app.add_middleware(SecurityHeadersMiddleware, enabled=enabled)

    @app.get("/api/ok")
    async def ok() -> dict[str, bool]:
        return {"ok": True}

    @app.get("/api/error")
    async def error() -> None:
        raise HTTPException(status_code=500, detail="controlled")

    return TestClient(app)


def assert_security_headers(response) -> None:
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert response.headers["Referrer-Policy"] == "no-referrer"
    assert response.headers["Cache-Control"] == "no-store"


def test_headers_are_present_on_success() -> None:
    response = create_client().get("/api/ok")
    assert response.status_code == 200
    assert_security_headers(response)


def test_headers_are_present_on_error() -> None:
    response = create_client().get("/api/error")
    assert response.status_code == 500
    assert_security_headers(response)


def test_headers_can_be_disabled() -> None:
    response = create_client(enabled=False).get("/api/ok")
    assert "X-Content-Type-Options" not in response.headers
    assert "X-Frame-Options" not in response.headers
    assert "Referrer-Policy" not in response.headers
    assert "Cache-Control" not in response.headers
