from copy import deepcopy
from decimal import Decimal

import pytest

from src.domain.models import (
    DecisionRule,
    Offer,
    PreferenceProfile,
    Recommendation,
    RecommendationScore,
    RuleOperator,
)
from src.domain.services import RuleEngine


def recommendation(
    provider: str = "amadeus",
    price: str = "100",
    duration: int | None = 90,
    stops: int | None = 0,
    score: str = "80",
    rank: int = 1,
) -> Recommendation:
    attributes: dict[str, int] = {}
    if duration is not None:
        attributes["total_duration_minutes"] = duration
    if stops is not None:
        attributes["stops"] = stops
    return Recommendation(
        offer=Offer(
            provider=provider,
            product_type="flight",
            price=Decimal(price),
            currency="BRL",
            attributes=attributes,
        ),
        score=RecommendationScore(
            overall_score=Decimal(score),
            price_score=Decimal("80"),
            duration_score=Decimal("80"),
            provider_score=Decimal("50"),
        ),
        rank=rank,
        profile=PreferenceProfile.balanced(),
        reasons=("Best balanced score",),
    )


def rule(
    field: str,
    operator: RuleOperator,
    value: str | Decimal | int | tuple[str, ...],
    *,
    enabled: bool = True,
) -> DecisionRule:
    return DecisionRule(
        rule_id=f"rule-{field}",
        rule_type="constraint",
        field=field,
        operator=operator,
        value=value,
        reason=f"Rejected by {field}",
        enabled=enabled,
    )


@pytest.mark.parametrize(
    ("field", "operator", "value"),
    [
        ("offer.price", RuleOperator.LESS_THAN_OR_EQUAL, Decimal("120")),
        ("offer.provider", RuleOperator.EQUALS, "amadeus"),
        ("offer.attributes.total_duration_minutes", RuleOperator.LESS_THAN, 120),
        ("offer.attributes.stops", RuleOperator.EQUALS, 0),
        ("recommendation.score.overall_score", RuleOperator.GREATER_THAN_OR_EQUAL, Decimal("75")),
    ],
)
def test_accepts_rules_for_supported_fields(
    field: str,
    operator: RuleOperator,
    value: str | Decimal | int,
) -> None:
    result = RuleEngine().evaluate(
        [recommendation()], [rule(field, operator, value)]
    )

    assert len(result.accepted) == 1
    assert result.rejected == ()


def test_supports_contains_and_in_operators() -> None:
    rules = [
        rule("offer.provider", RuleOperator.CONTAINS, "mad"),
        rule("offer.currency", RuleOperator.IN, ("BRL", "USD")),
    ]

    assert len(RuleEngine().evaluate([recommendation()], rules).accepted) == 1


def test_disabled_rule_is_ignored() -> None:
    disabled = rule(
        "offer.price", RuleOperator.LESS_THAN, Decimal("1"), enabled=False
    )

    assert len(RuleEngine().evaluate([recommendation()], [disabled]).accepted) == 1


def test_missing_field_rejects_without_error() -> None:
    result = RuleEngine().evaluate(
        [recommendation(duration=None)],
        [rule("offer.attributes.total_duration_minutes", RuleOperator.LESS_THAN, 120)],
    )

    assert result.accepted == ()
    assert result.rejected[0].reasons == (
        "Rejected by offer.attributes.total_duration_minutes",
    )


def test_returns_accepted_and_rejected_in_input_order_with_reasons() -> None:
    items = [
        recommendation("first", "90", rank=1),
        recommendation("expensive", "200", rank=2),
        recommendation("third", "100", rank=3),
    ]
    price_rule = rule(
        "offer.price", RuleOperator.LESS_THAN_OR_EQUAL, Decimal("120")
    )

    result = RuleEngine().evaluate(items, [price_rule])

    assert [item.offer.provider for item in result.accepted] == ["first", "third"]
    assert result.rejected[0].recommendation.offer.provider == "expensive"
    assert result.rejected[0].reasons == ("Rejected by offer.price",)


def test_does_not_modify_recommendations_or_rules() -> None:
    items = [recommendation()]
    rules = [rule("offer.provider", RuleOperator.NOT_EQUALS, "blocked")]
    original_items = deepcopy([item.model_dump() for item in items])
    original_rules = deepcopy([item.model_dump() for item in rules])

    RuleEngine().evaluate(items, rules)

    assert [item.model_dump() for item in items] == original_items
    assert [item.model_dump() for item in rules] == original_rules
