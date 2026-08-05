from decimal import Decimal

from fastapi.testclient import TestClient

from src.api.dependencies.travel import (
    get_compare_search_snapshots_use_case,
)
from src.application.travel.compare_search_snapshots import (
    NoComparableCurrencyError,
    SearchComparisonResult,
)
from src.main import app


client = TestClient(app)


def create_result() -> SearchComparisonResult:
    return SearchComparisonResult(
        base_search_id="base",
        target_search_id="target",
        currency="BRL",
        base_lowest_price=Decimal("100.00"),
        target_lowest_price=Decimal("80.00"),
        absolute_price_difference=Decimal("20.00"),
        percentage_price_difference=Decimal("-20.0"),
        base_best_provider="amadeus",
        target_best_provider="duffel",
        base_offer_count=2,
        target_offer_count=3,
        added_providers=("duffel",),
        removed_providers=(),
    )


class FakeComparisonUseCase:
    def __init__(
        self,
        result: SearchComparisonResult | None = None,
        error: Exception | None = None,
    ) -> None:
        self.result = result
        self.error = error

    async def execute(
        self,
        base_search_id: str,
        target_search_id: str,
    ) -> SearchComparisonResult | None:
        if self.error is not None:
            raise self.error
        return self.result


def test_search_comparison_serializes_decimal_values() -> None:
    app.dependency_overrides[
        get_compare_search_snapshots_use_case
    ] = lambda: FakeComparisonUseCase(create_result())
    try:
        response = client.get(
            "/api/v1/search-comparison",
            params={
                "base_search_id": "base",
                "target_search_id": "target",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    body = response.json()
    assert body["base_lowest_price"] == "100.00"
    assert body["target_lowest_price"] == "80.00"
    assert body["percentage_price_difference"] == "-20.0"
    assert body["added_providers"] == ["duffel"]


def test_search_comparison_returns_503_when_persistence_disabled() -> None:
    app.dependency_overrides[
        get_compare_search_snapshots_use_case
    ] = lambda: None
    try:
        response = client.get(
            "/api/v1/search-comparison",
            params={
                "base_search_id": "base",
                "target_search_id": "target",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 503
    assert response.json()["detail"]["code"] == (
        "search_persistence_disabled"
    )


def test_search_comparison_returns_404_when_snapshot_missing() -> None:
    app.dependency_overrides[
        get_compare_search_snapshots_use_case
    ] = lambda: FakeComparisonUseCase()
    try:
        response = client.get(
            "/api/v1/search-comparison",
            params={
                "base_search_id": "base",
                "target_search_id": "missing",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404


def test_search_comparison_returns_409_without_common_currency() -> None:
    error = NoComparableCurrencyError("No common currency.")
    app.dependency_overrides[
        get_compare_search_snapshots_use_case
    ] = lambda: FakeComparisonUseCase(error=error)
    try:
        response = client.get(
            "/api/v1/search-comparison",
            params={
                "base_search_id": "base",
                "target_search_id": "target",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 409
    assert response.json()["detail"]["code"] == (
        "no_comparable_currency"
    )
