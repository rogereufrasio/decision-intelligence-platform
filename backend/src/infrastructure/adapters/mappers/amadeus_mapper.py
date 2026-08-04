from datetime import datetime, timezone

from src.domain.entities.flight import (
    FlightOffer,
    FlightSlice,
    FlightSegment,
)


class AmadeusMapper:

    @staticmethod
    def to_flight_offer(data: dict) -> FlightOffer:
        offer_id = data.get("id")
        price = data.get("price", {})
        total_amount = price.get("grandTotal", "0.00")
        currency = price.get("currency", "BRL")

        slices = []
        total_duration = 0

        for slice_item in data.get("slices", []):
            segment_list = []
            slice_duration = 0

            for segment in slice_item.get("segments", []):
                departure_time = AmadeusMapper._to_utc_iso(
                    segment.get("departure", {}).get("at")
                )
                arrival_time = AmadeusMapper._to_utc_iso(
                    segment.get("arrival", {}).get("at")
                )
                duration = AmadeusMapper._to_duration_minutes(
                    segment.get("duration")
                )
                slice_duration += duration

                segment_list.append(
                    FlightSegment(
                        origin=segment.get("origin"),
                        destination=segment.get("destination"),
                        departure_time=departure_time,
                        arrival_time=arrival_time,
                        duration_minutes=duration,
                        carrier=segment.get("carrierCode"),
                        flight_number=segment.get("number"),
                    )
                )

            departure_date = AmadeusMapper._to_utc_iso(
                slice_item.get("departure", {}).get("at")
            )
            arrival_date = AmadeusMapper._to_utc_iso(
                slice_item.get("arrival", {}).get("at")
            )

            total_duration += slice_duration

            slices.append(
                FlightSlice(
                    origin=slice_item.get("origin"),
                    destination=slice_item.get("destination"),
                    departure_date=departure_date,
                    arrival_date=arrival_date,
                    duration_minutes=slice_duration,
                    segments=segment_list,
                )
            )

        return FlightOffer(
            id=offer_id,
            provider="amadeus",
            total_amount=str(total_amount),
            currency=currency,
            total_duration_minutes=total_duration,
            slices=slices,
        )

    @staticmethod
    def _to_utc_iso(value: str | None) -> str | None:
        if not value:
            return None

        try:
            parsed = datetime.fromisoformat(value)
        except ValueError:
            parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")

        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc).isoformat()

    @staticmethod
    def _to_duration_minutes(duration_iso: str | None) -> int:
        if not duration_iso:
            return 0

        # Amadeus duration comes as PT#H#M
        hours = 0
        minutes = 0
        if duration_iso.startswith("PT"):
            payload = duration_iso[2:]
            if "H" in payload:
                hours_part, payload = payload.split("H", 1)
                hours = int(hours_part)
            if "M" in payload:
                minutes_part = payload.replace("M", "")
                minutes = int(minutes_part)
        return hours * 60 + minutes
