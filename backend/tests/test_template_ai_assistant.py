from copy import deepcopy
from decimal import Decimal

import pytest

from src.application.ports import AIAssistant
from src.core.config import Settings
from src.domain.models import (
    AIContext,
    DecisionExplanation,
    PreferenceProfileName,
)
from src.infrastructure.ai import TemplateAIAssistant
from src.infrastructure.container import Container


def context_with_explanation() -> AIContext:
    return AIContext(
        decision_explanation=DecisionExplanation(
            summary="Selected the best eligible offer.",
            reasons=("Lowest price", "Preferred provider"),
            warnings=("One option was rejected",),
            rejected_count=1,
            profile=PreferenceProfileName.BALANCED,
        )
    )


@pytest.mark.asyncio
async def test_response_is_deterministic() -> None:
    assistant = TemplateAIAssistant()
    context = context_with_explanation()

    first = await assistant.explain(context, "prompt")
    second = await assistant.explain(context, "different prompt")

    assert first == second
    assert first.summary == "Selected the best eligible offer."
    assert first.confidence == Decimal("1")
    assert first.provider == "local"
    assert first.model == "template"


@pytest.mark.asyncio
async def test_preserves_reasons_and_warnings() -> None:
    result = await TemplateAIAssistant().explain(
        context_with_explanation(), "prompt"
    )

    assert result.reasons == ("Lowest price", "Preferred provider")
    assert result.warnings == ("One option was rejected",)


@pytest.mark.asyncio
async def test_handles_empty_context_without_inventing_facts() -> None:
    result = await TemplateAIAssistant().explain(AIContext(), "prompt")

    assert result.summary == "No decision context was provided."
    assert result.reasons == ()
    assert result.warnings == ()
    assert result.confidence == Decimal("0")


def test_container_returns_none_when_disabled() -> None:
    container = Container(Settings(ai_assistant_enabled=False))

    assert container.get_ai_assistant() is None


def test_container_returns_template_adapter() -> None:
    container = Container(Settings(
        ai_assistant_enabled=True,
        ai_assistant_provider="template",
    ))

    assert isinstance(container.get_ai_assistant(), TemplateAIAssistant)


def test_container_rejects_invalid_provider() -> None:
    container = Container(Settings(
        ai_assistant_enabled=True,
        ai_assistant_provider="unsupported",
    ))

    with pytest.raises(ValueError, match="Unsupported AI assistant provider"):
        container.get_ai_assistant()


def test_adapter_satisfies_protocol() -> None:
    assert isinstance(TemplateAIAssistant(), AIAssistant)


@pytest.mark.asyncio
async def test_does_not_modify_input() -> None:
    context = context_with_explanation()
    original = deepcopy(context.model_dump())

    await TemplateAIAssistant().explain(context, "prompt")

    assert context.model_dump() == original
