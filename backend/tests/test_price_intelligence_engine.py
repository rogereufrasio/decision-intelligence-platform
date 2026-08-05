from datetime import date, datetime, timedelta, timezone
from decimal import Decimal

from src.domain.models import Offer, PriceTrend, SearchCriteria, SearchSnapshot
from src.domain.services import PriceIntelligenceEngine


def create_snapshot(
    search_id: str,
    price: str | None,
    *,
    days_ago: int = 0,
    currency: str = "BRL",
    destination: str = "GRU",
) -> SearchSnapshot:
    offers = [] if price is None else [
        Offer(
            provider="provider",
            product_type="flight",
            price=Decimal(price),
            currency=currency,
        )
    ]
    return SearchSnapshot(
        search_id=search_id,
        criteria=SearchCriteria(
            origin="GIG",
            destination=destination,
            departure_date=date(2026, 9, 3),
            adults=1,
        ),
        created_at=datetime(2026, 8, 5, tzinfo=timezone.utc)
        - timedelta(days=days_ago),
        provider="aggregated",
        status="success",
        offers=offers,
    )


def test_detects_price_decrease() -> None:
    result = PriceIntelligenceEngine().analyze([
        create_snapshot("current", "90"),
        create_snapshot("previous", "100", days_ago=1),
    ])

    assert result.trend == PriceTrend.DECREASED
    assert result.absolute_change == Decimal("-10")
    assert result.percentage_change == Decimal("-10.0")


def test_detects_price_increase() -> None:
    result = PriceIntelligenceEngine().analyze([
        create_snapshot("current", "110"),
        create_snapshot("previous", "100", days_ago=1),
    ])

    assert result.trend == PriceTrend.INCREASED
    assert result.percentage_change == Decimal("10.0")


def test_classifies_change_below_one_percent_as_stable() -> None:
    result = PriceIntelligenceEngine().analyze([
        create_snapshot("current", "100.50"),
        create_snapshot("previous", "100", days_ago=1),
    ])

    assert result.trend == PriceTrend.STABLE


def test_calculates_historical_statistics_from_lowest_prices() -> None:
    current = create_snapshot("current", "90")
    current = current.model_copy(update={
        "offers": [
            *current.offers,
            Offer(provider="other", product_type="flight", price=Decimal("120"), currency="BRL"),
        ]
    })
    result = PriceIntelligenceEngine().analyze([
        current,
        create_snapshot("previous", "100", days_ago=1),
        create_snapshot("oldest", "80", days_ago=2),
    ])

    assert result.current_price == Decimal("90")
    assert result.previous_price == Decimal("100")
    assert result.historical_min == Decimal("80")
    assert result.historical_max == Decimal("100")
    assert result.historical_average == Decimal("90")
    assert result.snapshot_count == 3
    assert result.currency == "BRL"


def test_ignores_different_currencies_and_criteria() -> None:
    result = PriceIntelligenceEngine().analyze([
        create_snapshot("current", "90"),
        create_snapshot("usd", "10", days_ago=1, currency="USD"),
        create_snapshot("other-route", "20", days_ago=1, destination="BSB"),
        create_snapshot("previous", "100", days_ago=2),
    ])

    assert result.snapshot_count == 2
    assert result.historical_min == Decimal("90")


def test_ignores_snapshot_without_offers() -> None:
    result = PriceIntelligenceEngine().analyze([
        create_snapshot("current", "90"),
        create_snapshot("empty", None, days_ago=1),
        create_snapshot("previous", "100", days_ago=2),
    ])

    assert result.snapshot_count == 2


def test_empty_and_single_history_are_insufficient() -> None:
    engine = PriceIntelligenceEngine()

    assert engine.analyze([]).trend == PriceTrend.INSUFFICIENT_DATA
    single = engine.analyze([create_snapshot("only", "90")])
    assert single.trend == PriceTrend.INSUFFICIENT_DATA
    assert single.snapshot_count == 1


def test_does_not_modify_snapshots() -> None:
    snapshots = [
        create_snapshot("current", "90"),
        create_snapshot("previous", "100", days_ago=1),
    ]
    original = [snapshot.model_dump() for snapshot in snapshots]

    PriceIntelligenceEngine().analyze(snapshots)

    assert [snapshot.model_dump() for snapshot in snapshots] == original
