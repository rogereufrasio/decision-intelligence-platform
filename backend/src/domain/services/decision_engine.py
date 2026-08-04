from __future__ import annotations

from src.domain.entities.decision import SortCriterion
from src.domain.entities.flight import FlightOffer


class DecisionEngine:

    @staticmethod
    def rank_offers(
        offers: list[FlightOffer],
        criterion: SortCriterion,
    ) -> list[FlightOffer]:
        normalized = DecisionEngine._deduplicate_offers(offers)

        if criterion == SortCriterion.CHEAPEST:
            return sorted(
                normalized,
                key=lambda offer: float(offer.total_amount),
            )

        if criterion == SortCriterion.FASTEST:
            return sorted(
                normalized,
                key=lambda offer: offer.total_duration_minutes,
            )

        if criterion == SortCriterion.BEST_VALUE:
            return DecisionEngine._rank_by_best_value(normalized)

        return normalized

    @staticmethod
    def _deduplicate_offers(
        offers: list[FlightOffer],
    ) -> list[FlightOffer]:
        best_map: dict[str, FlightOffer] = {}

        for offer in offers:
            key = DecisionEngine._offer_key(offer)
            existing = best_map.get(key)

            if existing is None:
                best_map[key] = offer
                continue

            if float(offer.total_amount) < float(existing.total_amount):
                best_map[key] = offer

        return list(best_map.values())

    @staticmethod
    def _offer_key(offer: FlightOffer) -> str:
        if not offer.slices:
            return f"{offer.provider}|{offer.total_amount}|{offer.currency}"

        slice_keys = []
        for slice_item in offer.slices:
            segment_keys = []
            for segment in slice_item.segments:
                segment_keys.append(
                    f"{segment.origin}-{segment.destination}-"
                    f"{segment.departure_time}-"
                    f"{segment.arrival_time}-"
                    f"{segment.flight_number or ''}-"
                    f"{segment.carrier or ''}"
                )
            slice_keys.append(
                f"{slice_item.origin}-{slice_item.destination}-"
                f"{slice_item.departure_date}-"
                f"{slice_item.arrival_date}|{'|'.join(segment_keys)}"
            )
        return f"{offer.provider}|{offer.currency}|{'|'.join(slice_keys)}"

    @staticmethod
    def _rank_by_best_value(
        offers: list[FlightOffer],
    ) -> list[FlightOffer]:
        if not offers:
            return []

        prices = [float(offer.total_amount) for offer in offers]
        durations = [offer.total_duration_minutes for offer in offers]

        min_price = min(prices)
        max_price = max(prices)
        min_duration = min(durations)
        max_duration = max(durations)

        def score(offer: FlightOffer) -> float:
            normalized_price = (
                (float(offer.total_amount) - min_price) /
                (max_price - min_price)
                if max_price > min_price else 0.0
            )
            normalized_duration = (
                (offer.total_duration_minutes - min_duration) /
                (max_duration - min_duration)
                if max_duration > min_duration else 0.0
            )
            return 100 - (normalized_price * 60 + normalized_duration * 40)

        return sorted(offers, key=score, reverse=True)
