from decimal import Decimal

from src.application.travel.recommend_travel_offers import (
    RecommendTravelOffersUseCase,
)
from src.domain.models import Offer, PreferenceProfile
from src.domain.services import RecommendationEngine


def create_offer(provider: str, price: str, duration: int) -> Offer:
    return Offer(
        provider=provider,
        product_type="flight",
        price=Decimal(price),
        currency="BRL",
        attributes={"total_duration_minutes": duration},
    )


def test_use_case_recommends_cheapest_offer() -> None:
    offers = [
        create_offer("expensive", "200", 60),
        create_offer("cheap", "100", 180),
    ]
    use_case = RecommendTravelOffersUseCase(RecommendationEngine())

    result = use_case.execute(offers, PreferenceProfile.cheapest())

    assert result[0].offer.provider == "cheap"


def test_use_case_recommends_fastest_offer() -> None:
    offers = [
        create_offer("slow", "100", 180),
        create_offer("fast", "200", 60),
    ]
    use_case = RecommendTravelOffersUseCase(RecommendationEngine())

    result = use_case.execute(offers, PreferenceProfile.fastest())

    assert result[0].offer.provider == "fast"


def test_use_case_applies_preferred_providers() -> None:
    offers = [
        create_offer("standard", "100", 100),
        create_offer("premium", "130", 110),
    ]
    use_case = RecommendTravelOffersUseCase(RecommendationEngine())

    result = use_case.execute(
        offers,
        PreferenceProfile.premium(),
        preferred_providers=["premium"],
    )

    assert result[0].offer.provider == "premium"
    assert result[0].score.provider_score == Decimal("100")
