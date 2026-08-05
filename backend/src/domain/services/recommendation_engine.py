from decimal import Decimal

from src.domain.models.offer import Offer
from src.domain.models.preference_profile import (
    PreferenceProfile,
    PreferenceProfileName,
)
from src.domain.models.recommendation import Recommendation
from src.domain.models.recommendation_score import RecommendationScore


class RecommendationEngine:
    NEUTRAL_SCORE = Decimal("50")
    MINIMUM_SCORE = Decimal("0")
    MAXIMUM_SCORE = Decimal("100")

    def recommend(
        self,
        offers: list[Offer],
        profile: PreferenceProfile,
    ) -> list[Recommendation]:
        if not offers:
            return []

        prices = [offer.price for offer in offers]
        durations = [self._duration(offer) for offer in offers]
        available_durations = [
            duration for duration in durations if duration is not None
        ]
        minimum_price = min(prices)
        maximum_price = max(prices)
        minimum_duration = (
            min(available_durations) if available_durations else None
        )
        maximum_duration = (
            max(available_durations) if available_durations else None
        )
        preferred_providers = set(profile.preferred_providers)

        scored_offers = []
        for offer, duration in zip(offers, durations, strict=True):
            price_score = self._normalize_inverse(
                offer.price,
                minimum_price,
                maximum_price,
            )
            duration_score = self._duration_score(
                duration,
                minimum_duration,
                maximum_duration,
            )
            provider_score = self._provider_score(
                offer.provider,
                preferred_providers,
            )
            overall_score = self._clamp(
                price_score * profile.price_weight
                + duration_score * profile.duration_weight
                + provider_score * profile.provider_weight
            )
            reasons = self._reasons(
                offer=offer,
                duration=duration,
                minimum_price=minimum_price,
                minimum_duration=minimum_duration,
                preferred_providers=preferred_providers,
            )
            score = RecommendationScore(
                overall_score=overall_score,
                price_score=price_score,
                duration_score=duration_score,
                provider_score=provider_score,
            )
            scored_offers.append((offer, duration, score, reasons))

        scored_offers.sort(
            key=lambda item: (
                -item[2].overall_score,
                item[0].price,
                self._duration_sort_value(item[1]),
                item[0].provider,
            )
        )

        recommendations = []
        for index, (offer, _, score, reasons) in enumerate(
            scored_offers,
            start=1,
        ):
            ranked_reasons = reasons
            if (
                index == 1
                and profile.name is PreferenceProfileName.BALANCED
            ):
                ranked_reasons = (*reasons, "Best balanced score")

            recommendations.append(
                Recommendation(
                    offer=offer,
                    score=score,
                    rank=index,
                    profile=profile,
                    reasons=ranked_reasons,
                )
            )

        return recommendations

    def _duration_score(
        self,
        duration: Decimal | None,
        minimum_duration: Decimal | None,
        maximum_duration: Decimal | None,
    ) -> Decimal:
        if (
            duration is None
            or minimum_duration is None
            or maximum_duration is None
        ):
            return self.NEUTRAL_SCORE

        return self._normalize_inverse(
            duration,
            minimum_duration,
            maximum_duration,
        )

    def _provider_score(
        self,
        provider: str,
        preferred_providers: set[str],
    ) -> Decimal:
        if not preferred_providers:
            return self.NEUTRAL_SCORE
        if provider in preferred_providers:
            return self.MAXIMUM_SCORE
        return self.MINIMUM_SCORE

    def _normalize_inverse(
        self,
        value: Decimal,
        minimum: Decimal,
        maximum: Decimal,
    ) -> Decimal:
        if minimum == maximum:
            return self.MAXIMUM_SCORE

        normalized = self.MAXIMUM_SCORE - (
            (value - minimum)
            / (maximum - minimum)
            * self.MAXIMUM_SCORE
        )
        return self._clamp(normalized)

    def _reasons(
        self,
        offer: Offer,
        duration: Decimal | None,
        minimum_price: Decimal,
        minimum_duration: Decimal | None,
        preferred_providers: set[str],
    ) -> tuple[str, ...]:
        reasons = []
        if offer.price == minimum_price:
            reasons.append("Lowest price")
        if duration is not None and duration == minimum_duration:
            reasons.append("Shortest duration")
        if offer.provider in preferred_providers:
            reasons.append("Preferred provider")
        return tuple(reasons)

    @staticmethod
    def _duration(offer: Offer) -> Decimal | None:
        if not offer.attributes:
            return None

        value = offer.attributes.get("total_duration_minutes")
        if isinstance(value, bool) or not isinstance(
            value,
            (int, float, Decimal),
        ):
            return None

        return Decimal(str(value))

    @staticmethod
    def _duration_sort_value(duration: Decimal | None) -> Decimal:
        return duration if duration is not None else Decimal("Infinity")

    def _clamp(self, value: Decimal) -> Decimal:
        return min(
            self.MAXIMUM_SCORE,
            max(self.MINIMUM_SCORE, value),
        )
