from decimal import Decimal

from src.domain.models import PreferenceProfile, RejectedRecommendation
from src.domain.services import DecisionExplanationEngine
from tests.test_rule_engine import recommendation


def test_explains_best_accepted_recommendation() -> None:
    selected = recommendation("best", "90")
    rejected = RejectedRecommendation(
        recommendation=recommendation("blocked", "200"),
        reasons=("Too expensive",),
    )

    result = DecisionExplanationEngine().explain(
        (selected,), (rejected,), PreferenceProfile.balanced()
    )

    assert result.selected_offer == selected.offer
    assert result.selected_provider == "best"
    assert result.selected_price == Decimal("90")
    assert result.selected_currency == "BRL"
    assert result.reasons == selected.reasons
    assert result.rejected_count == 1
    assert result.warnings == ("Decision rules eliminated 1 option(s).",)


def test_explains_when_no_recommendation_is_accepted() -> None:
    rejected = RejectedRecommendation(
        recommendation=recommendation(), reasons=("Blocked",)
    )

    result = DecisionExplanationEngine().explain(
        (), (rejected,), PreferenceProfile.cheapest()
    )

    assert result.selected_offer is None
    assert result.selected_provider is None
    assert result.selected_price is None
    assert result.summary == "No recommendation satisfies the decision rules."
