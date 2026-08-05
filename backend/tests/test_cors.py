from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


def test_cors_preflight_allows_configured_frontend_origin() -> None:
    response = client.options(
        "/api/v1/flights/search",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": (
                "content-type,x-travel-provider,x-correlation-id"
            ),
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == (
        "http://localhost:5173"
    )
    assert response.headers.get("access-control-allow-credentials") is None


def test_cors_does_not_allow_unknown_origin() -> None:
    response = client.options(
        "/api/v1/flights/search",
        headers={
            "Origin": "https://untrusted.example",
            "Access-Control-Request-Method": "POST",
        },
    )

    assert "access-control-allow-origin" not in response.headers
