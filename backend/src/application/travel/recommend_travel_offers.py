from collections.abc import Sequence

from src.domain.models import Offer, PreferenceProfile, Recommendation
from src.domain.services import RecommendationEngine


class RecommendTravelOffersUseCase:
    def __init__(self, engine: RecommendationEngine) -> None:
        self.engine = engine

    def execute(
        self,
        offers: list[Offer],
        profile: PreferenceProfile,
        preferred_providers: Sequence[str] | None = None,
    ) -> list[Recommendation]:
        effective_profile = profile
        if preferred_providers is not None:
            effective_profile = PreferenceProfile(
                name=profile.name,
                price_weight=profile.price_weight,
                duration_weight=profile.duration_weight,
                provider_weight=profile.provider_weight,
                preferred_providers=tuple(preferred_providers),
            )

        return self.engine.recommend(offers, effective_profile)
