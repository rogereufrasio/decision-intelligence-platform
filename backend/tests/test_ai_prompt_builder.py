from copy import deepcopy
from decimal import Decimal

from src.domain.models import AIContext, PriceIntelligence, PriceTrend
from src.domain.services import AIPromptBuilder


def test_builds_deterministic_prompt_from_context() -> None:
    context = AIContext(
        price_intelligence=PriceIntelligence(
            current_price=Decimal("90.50"),
            previous_price=Decimal("100"),
            absolute_change=Decimal("-9.50"),
            percentage_change=Decimal("-9.5"),
            trend=PriceTrend.DECREASED,
            snapshot_count=2,
            currency="BRL",
        )
    )

    first = AIPromptBuilder().build(context)
    second = AIPromptBuilder().build(context)

    assert first == second
    assert '"current_price":"90.50"' in first
    assert '"trend":"decreased"' in first
    assert "Do not invent facts" in first


def test_builds_prompt_for_empty_context_without_error() -> None:
    prompt = AIPromptBuilder().build(AIContext())

    assert prompt.endswith("Context: {}")


def test_does_not_modify_context() -> None:
    context = AIContext(
        price_intelligence=PriceIntelligence(
            trend=PriceTrend.INSUFFICIENT_DATA,
            snapshot_count=0,
        )
    )
    original = deepcopy(context.model_dump())

    AIPromptBuilder().build(context)

    assert context.model_dump() == original
