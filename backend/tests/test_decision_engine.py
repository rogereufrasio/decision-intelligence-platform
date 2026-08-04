import pytest

from src.domain.entities.decision import SortCriterion
from src.domain.entities.flight import (
    FlightOffer,
    FlightSlice,
    FlightSegment,
)
from src.domain.services.decision_engine import DecisionEngine


def create_offer(
    offer_id: str,
    price: str,
    duration: int,
    origin: str = "GIG",
    destination: str = "GRU",
    flight_number: str | None = None,
) -> FlightOffer:
    if flight_number is None:
        flight_number = f"AB{offer_id}"

    return FlightOffer(
        id=offer_id,
        provider="test",
        total_amount=price,
        currency="BRL",
        total_duration_minutes=duration,
        slices=[
            FlightSlice(
                origin=origin,
                destination=destination,
                departure_date="2026-10-01T10:00:00+00:00",
                arrival_date="2026-10-01T12:00:00+00:00",
                duration_minutes=duration,
                segments=[
                    FlightSegment(
                        origin=origin,
                        destination=destination,
                        departure_time="2026-10-01T10:00:00+00:00",
                        arrival_time="2026-10-01T12:00:00+00:00",
                        duration_minutes=duration,
                        carrier="LA",
                        flight_number=flight_number,
                    )
                ],
            )
        ],
    )


def test_rank_offers_by_cheapest():
    offers = [
        create_offer("1", "300.00", 180),
        create_offer("2", "200.00", 240),
    ]

    ranked = DecisionEngine.rank_offers(
        offers,
        SortCriterion.CHEAPEST,
    )

    assert ranked[0].id == "2"
    assert ranked[1].id == "1"


def test_rank_offers_by_fastest():
    offers = [
        create_offer("1", "300.00", 180),
        create_offer("2", "200.00", 120),
    ]

    ranked = DecisionEngine.rank_offers(
        offers,
        SortCriterion.FASTEST,
    )

    assert ranked[0].id == "2"
    assert ranked[1].id == "1"


def test_rank_offers_by_best_value():
    offers = [
        create_offer("1", "100.00", 300),
        create_offer("2", "200.00", 120),
    ]

    ranked = DecisionEngine.rank_offers(
        offers,
        SortCriterion.BEST_VALUE,
    )

    assert ranked[0].id == "1"
    assert ranked[1].id == "2"


def test_deduplicate_offers_chooses_cheapest():
    offers = [
        create_offer("1", "200.00", 180, flight_number="AB1"),
        create_offer("2", "150.00", 180, flight_number="AB1"),
    ]

    offers[1].slices[0].departure_date = offers[0].slices[0].departure_date
    offers[1].slices[0].arrival_date = offers[0].slices[0].arrival_date

    ranked = DecisionEngine.rank_offers(
        offers,
        SortCriterion.CHEAPEST,
    )

    assert len(ranked) == 1
    assert ranked[0].id == "2"
