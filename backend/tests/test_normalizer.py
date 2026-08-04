import pytest

from src.infrastructure.adapters.mappers.amadeus_mapper import AmadeusMapper
from src.infrastructure.adapters.mappers.duffel_mapper import DuffelMapper


def test_amadeus_mapper_transforms_payload():
    payload = {
        "id": "offer-1",
        "price": {
            "grandTotal": "450.00",
            "currency": "USD",
        },
        "slices": [
            {
                "origin": "GIG",
                "destination": "GRU",
                "departure": {"at": "2026-10-01T10:00:00"},
                "arrival": {"at": "2026-10-01T12:30:00"},
                "segments": [
                    {
                        "origin": "GIG",
                        "destination": "GRU",
                        "departure": {"at": "2026-10-01T10:00:00"},
                        "arrival": {"at": "2026-10-01T12:30:00"},
                        "duration": "PT2H30M",
                        "carrierCode": "LA",
                        "number": "1234",
                    }
                ],
            }
        ],
    }

    result = AmadeusMapper.to_flight_offer(payload)

    assert result.id == "offer-1"
    assert result.provider == "amadeus"
    assert result.total_amount == "450.00"
    assert result.currency == "USD"
    assert result.total_duration_minutes == 150
    assert len(result.slices) == 1
    assert result.slices[0].duration_minutes == 150
    assert result.slices[0].departure_date.endswith("+00:00")
    assert result.slices[0].segments[0].carrier == "LA"
    assert result.slices[0].segments[0].flight_number == "1234"


def test_duffel_mapper_transforms_payload():
    payload = {
        "id": "duffel-offer-1",
        "total_amount": "520.00",
        "total_currency": "EUR",
        "slices": [
            {
                "origin": "GIG",
                "destination": "GRU",
                "departure": "2026-10-01T10:00:00+00:00",
                "arrival": "2026-10-01T12:30:00+00:00",
                "segments": [
                    {
                        "origin": "GIG",
                        "destination": "GRU",
                        "departure": "2026-10-01T10:00:00+00:00",
                        "arrival": "2026-10-01T12:30:00+00:00",
                        "duration": "PT2H30M",
                        "carrier": "LA",
                        "flight_number": "1234",
                    }
                ],
            }
        ],
    }

    result = DuffelMapper.to_flight_offer(payload)

    assert result.id == "duffel-offer-1"
    assert result.provider == "duffel"
    assert result.total_amount == "520.00"
    assert result.currency == "EUR"
    assert result.total_duration_minutes == 150
    assert len(result.slices) == 1
    assert result.slices[0].departure_date.endswith("+00:00")
    assert result.slices[0].segments[0].flight_number == "1234"
    assert result.slices[0].segments[0].carrier == "LA"
