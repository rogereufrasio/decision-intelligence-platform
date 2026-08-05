from __future__ import annotations

from src.domain.entities.decision import SortCriterion
from src.domain.models import Offer


class DecisionEngine:

    @staticmethod
    def rank_offers(
        offers: list[Offer],
        criterion: SortCriterion | None,
    ) -> list[Offer]:
        normalized = DecisionEngine._deduplicate_offers(offers)

        if criterion == SortCriterion.CHEAPEST:
            return sorted(
                normalized,
                key=lambda offer: float(offer.price),
            )

        if criterion == SortCriterion.FASTEST:
            return sorted(
                normalized,
                key=DecisionEngine._total_duration_minutes,
            )

        if criterion == SortCriterion.BEST_VALUE:
            return DecisionEngine._rank_by_best_value(normalized)

        return normalized

    @staticmethod
    def _deduplicate_offers(
        offers: list[Offer],
    ) -> list[Offer]:
        best_map: dict[str, Offer] = {}

        for offer in offers:
            key = DecisionEngine._offer_key(offer)
            existing = best_map.get(key)

            if existing is None:
                best_map[key] = offer
                continue

            if float(offer.price) < float(existing.price):
                best_map[key] = offer

        return list(best_map.values())

    @staticmethod
    def _offer_key(offer: Offer) -> str:
        slices = (
            offer.attributes.get("slices")
            if offer.attributes and isinstance(offer.attributes, dict)
            else None
        )

        if not slices:
            return f"{offer.provider}|{offer.price}|{offer.currency}"

        slice_keys = []
        for slice_item in slices:
            if not isinstance(slice_item, dict):
                continue

            segment_keys = []
            for segment in slice_item.get("segments", []):
                if not isinstance(segment, dict):
                    continue
                segment_keys.append(
                    f"{segment.get('origin', '')}-{segment.get('destination', '')}-"
                    f"{segment.get('departure_time', '')}-"
                    f"{segment.get('arrival_time', '')}-"
                    f"{segment.get('flight_number', '') or ''}-"
                    f"{segment.get('carrier', '') or ''}"
                )
            slice_keys.append(
                f"{slice_item.get('origin', '')}-{slice_item.get('destination', '')}-"
                f"{slice_item.get('departure_date', '')}-"
                f"{slice_item.get('arrival_date', '')}|{'|'.join(segment_keys)}"
            )

        return f"{offer.provider}|{offer.currency}|{'|'.join(slice_keys)}"

    @staticmethod
    def _total_duration_minutes(offer: Offer) -> int:
        if offer.attributes and isinstance(offer.attributes, dict):
            duration = offer.attributes.get("total_duration_minutes")
            if isinstance(duration, (int, float)):
                return int(duration)

            slices = offer.attributes.get("slices")
            if isinstance(slices, list):
                total = 0
                for slice_item in slices:
                    if not isinstance(slice_item, dict):
                        continue
                    slice_duration = slice_item.get("duration_minutes")
                    if isinstance(slice_duration, (int, float)):
                        total += int(slice_duration)
                if total > 0:
                    return total

        return 0

    @staticmethod
    def _rank_by_best_value(
        offers: list[Offer],
    ) -> list[Offer]:
        if not offers:
            return []

        prices = [float(offer.price) for offer in offers]
        durations = [DecisionEngine._total_duration_minutes(offer) for offer in offers]

        min_price = min(prices)
        max_price = max(prices)
        min_duration = min(durations)
        max_duration = max(durations)

        def score(offer: Offer) -> float:
            normalized_price = (
                (float(offer.price) - min_price) /
                (max_price - min_price)
                if max_price > min_price else 0.0
            )
            normalized_duration = (
                (DecisionEngine._total_duration_minutes(offer) - min_duration) /
                (max_duration - min_duration)
                if max_duration > min_duration else 0.0
            )
            return 100 - (normalized_price * 60 + normalized_duration * 40)

        return sorted(offers, key=score, reverse=True)
