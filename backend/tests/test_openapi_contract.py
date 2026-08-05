from src.main import app


def test_openapi_contains_main_mvp_endpoints() -> None:
    schema = app.openapi()

    assert schema["openapi"]
    expected_operations = {
        ("/api/v1/health", "get"),
        ("/api/v1/readiness", "get"),
        ("/api/v1/metrics", "get"),
        ("/api/v1/travel/search", "post"),
        ("/api/v1/flights/search", "post"),
        ("/api/v1/recommendations", "post"),
        ("/api/v1/search-history", "get"),
        ("/api/v1/search-comparison", "get"),
        ("/api/v1/search-history/{search_id}/export", "get"),
        ("/api/v1/price-intelligence/{search_id}", "get"),
        ("/api/v1/decision-history", "get"),
        ("/api/v1/ai-explanations", "post"),
    }

    for path, method in expected_operations:
        assert path in schema["paths"]
        assert method in schema["paths"][path]
