from decimal import Decimal

from src.application.travel.evaluate_recommendations import (
    EvaluateRecommendationsUseCase,
)
from src.domain.models import PreferenceProfile, RuleOperator
from src.domain.services import DecisionExplanationEngine, RuleEngine
from tests.test_rule_engine import recommendation, rule


def test_evaluates_rules_and_builds_explanation() -> None:
    items = [
        recommendation("accepted", "90", rank=1),
        recommendation("rejected", "200", rank=2),
    ]
    use_case = EvaluateRecommendationsUseCase(
        RuleEngine(), DecisionExplanationEngine()
    )

    result = use_case.execute(
        items,
        [rule("offer.price", RuleOperator.LESS_THAN, Decimal("150"))],
        PreferenceProfile.balanced(),
    )

    assert result.accepted == (items[0],)
    assert result.rejected[0].recommendation == items[1]
    assert result.explanation.selected_offer == items[0].offer


def test_preserves_order_of_accepted_recommendations() -> None:
    items = [
        recommendation("one", "100", rank=1),
        recommendation("two", "110", rank=2),
    ]
    result = EvaluateRecommendationsUseCase(
        RuleEngine(), DecisionExplanationEngine()
    ).execute(items, [], PreferenceProfile.balanced())

    assert result.accepted == tuple(items)
