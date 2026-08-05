from copy import deepcopy
from decimal import Decimal

from src.domain.models import Offer, PreferenceProfile
from src.domain.services import RecommendationEngine


def create_offer(
    provider: str,
    price: str,
    duration: int | None,
) -> Offer:
    attributes = (
        {"total_duration_minutes": duration}
        if duration is not None
        else None
    )
    return Offer(
        provider=provider,
        product_type="flight",
        price=Decimal(price),
        currency="BRL",
        attributes=attributes,
    )


def test_cheapest_profile_prioritizes_lowest_price() -> None:
    offers = [
        create_offer("fast", "200", 60),
        create_offer("cheap", "100", 180),
    ]

    result = RecommendationEngine().recommend(
        offers,
        PreferenceProfile.cheapest(),
    )

    assert result[0].offer.provider == "cheap"
    assert result[0].score.price_score == Decimal("100")


def test_fastest_profile_prioritizes_shortest_duration() -> None:
    offers = [
        create_offer("slow", "100", 180),
        create_offer("fast", "200", 60),
    ]

    result = RecommendationEngine().recommend(
        offers,
        PreferenceProfile.fastest(),
    )

    assert result[0].offer.provider == "fast"
    assert result[0].score.duration_score == Decimal("100")


def test_balanced_profile_combines_price_and_duration() -> None:
    offers = [
        create_offer("cheap-slow", "100", 240),
        create_offer("balanced", "130", 120),
        create_offer("fast-expensive", "200", 60),
    ]

    result = RecommendationEngine().recommend(
        offers,
        PreferenceProfile.balanced(),
    )

    assert result[0].offer.provider == "balanced"
    assert "Best balanced score" in result[0].reasons


def test_premium_profile_values_preferred_provider() -> None:
    offers = [
        create_offer("standard", "100", 100),
        create_offer("premium", "130", 110),
    ]

    result = RecommendationEngine().recommend(
        offers,
        PreferenceProfile.premium(("premium",)),
    )

    assert result[0].offer.provider == "premium"
    assert result[0].score.provider_score == Decimal("100")
    assert "Preferred provider" in result[0].reasons


def test_all_scores_remain_between_zero_and_one_hundred() -> None:
    offers = [
        create_offer("one", "0", 0),
        create_offer("two", "999999", 999999),
        create_offer("three", "50", None),
    ]

    result = RecommendationEngine().recommend(
        offers,
        PreferenceProfile.balanced(),
    )

    for recommendation in result:
        scores = recommendation.score.model_dump().values()
        assert all(Decimal("0") <= score <= Decimal("100") for score in scores)


def test_equal_prices_receive_equal_scores() -> None:
    offers = [
        create_offer("one", "100", 60),
        create_offer("two", "100", 120),
    ]

    result = RecommendationEngine().recommend(
        offers,
        PreferenceProfile.cheapest(),
    )

    assert result[0].score.price_score == result[1].score.price_score


def test_equal_durations_receive_equal_scores() -> None:
    offers = [
        create_offer("one", "100", 60),
        create_offer("two", "200", 60),
    ]

    result = RecommendationEngine().recommend(
        offers,
        PreferenceProfile.fastest(),
    )

    assert result[0].score.duration_score == result[1].score.duration_score


def test_missing_duration_receives_neutral_score() -> None:
    offer = create_offer("unknown", "100", None)

    result = RecommendationEngine().recommend(
        [offer],
        PreferenceProfile.fastest(),
    )

    assert result[0].score.duration_score == Decimal("50")
    assert "Shortest duration" not in result[0].reasons


def test_no_preferred_provider_uses_neutral_score() -> None:
    offers = [
        create_offer("one", "100", 60),
        create_offer("two", "200", 120),
    ]

    result = RecommendationEngine().recommend(
        offers,
        PreferenceProfile.premium(),
    )

    assert all(
        recommendation.score.provider_score == Decimal("50")
        for recommendation in result
    )


def test_tie_breaking_is_deterministic() -> None:
    offers = [
        create_offer("zeta", "100", 60),
        create_offer("alpha", "100", 60),
    ]

    result = RecommendationEngine().recommend(
        offers,
        PreferenceProfile.balanced(),
    )

    assert [item.offer.provider for item in result] == ["alpha", "zeta"]
    assert [item.rank for item in result] == [1, 2]


def test_empty_offer_list_returns_empty_list() -> None:
    assert RecommendationEngine().recommend(
        [],
        PreferenceProfile.balanced(),
    ) == []


def test_input_offers_are_not_modified() -> None:
    offers = [
        create_offer("one", "100", 60),
        create_offer("two", "200", 120),
    ]
    original_values = deepcopy(
        [offer.model_dump() for offer in offers]
    )
    original_order = list(offers)

    RecommendationEngine().recommend(
        offers,
        PreferenceProfile.balanced(),
    )

    assert offers == original_order
    assert [offer.model_dump() for offer in offers] == original_values


def test_reasons_correspond_to_recommendation_attributes() -> None:
    offers = [
        create_offer("preferred", "100", 60),
        create_offer("other", "200", 120),
    ]

    result = RecommendationEngine().recommend(
        offers,
        PreferenceProfile.premium(("preferred",)),
    )

    assert result[0].reasons == (
        "Lowest price",
        "Shortest duration",
        "Preferred provider",
    )
