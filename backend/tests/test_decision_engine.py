import pytest

from src.domain.entities.decision import SortCriterion
from src.domain.models import Offer
from src.domain.services.decision_engine import DecisionEngine


def create_offer(
    offer_id: str,
    price: str,
    duration: int,
    origin: str = "GIG",
    destination: str = "GRU",
    flight_number: str | None = None,
) -> Offer:
    if flight_number is None:
        flight_number = f"AB{offer_id}"

    return Offer(
        provider="test",
        product_type="flight",
        price=price,
        currency="BRL",
        metadata={
            "id": offer_id,
        },
        attributes={
            "total_duration_minutes": duration,
            "slices": [
                {
                    "origin": origin,
                    "destination": destination,
                    "departure_date": "2026-10-01T10:00:00+00:00",
                    "arrival_date": "2026-10-01T12:00:00+00:00",
                    "duration_minutes": duration,
                    "segments": [
                        {
                            "origin": origin,
                            "destination": destination,
                            "departure_time": "2026-10-01T10:00:00+00:00",
                            "arrival_time": "2026-10-01T12:00:00+00:00",
                            "duration_minutes": duration,
                            "carrier": "LA",
                            "flight_number": flight_number,
                        }
                    ],
                }
            ],
        },
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

    assert ranked[0].metadata["id"] == "2"
    assert ranked[1].metadata["id"] == "1"


def test_rank_offers_by_fastest():
    offers = [
        create_offer("1", "300.00", 180),
        create_offer("2", "200.00", 120),
    ]

    ranked = DecisionEngine.rank_offers(
        offers,
        SortCriterion.FASTEST,
    )

    assert ranked[0].metadata["id"] == "2"
    assert ranked[1].metadata["id"] == "1"


def test_rank_offers_by_best_value():
    offers = [
        create_offer("1", "100.00", 300),
        create_offer("2", "200.00", 120),
    ]

    ranked = DecisionEngine.rank_offers(
        offers,
        SortCriterion.BEST_VALUE,
    )

    assert ranked[0].metadata["id"] == "1"
    assert ranked[1].metadata["id"] == "2"


def test_deduplicate_offers_chooses_cheapest():
    offers = [
        create_offer("1", "200.00", 180, flight_number="AB1"),
        create_offer("2", "150.00", 180, flight_number="AB1"),
    ]

    first_slice = offers[0].attributes["slices"][0]
    second_slice = offers[1].attributes["slices"][0]
    second_slice["departure_date"] = first_slice["departure_date"]
    second_slice["arrival_date"] = first_slice["arrival_date"]

    ranked = DecisionEngine.rank_offers(
        offers,
        SortCriterion.CHEAPEST,
    )

    assert len(ranked) == 1
    assert ranked[0].metadata["id"] == "2"
