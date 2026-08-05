import pytest

from src.application.travel.explain_decision import ExplainDecisionUseCase
from src.domain.models import AIContext, AIExplanation
from src.domain.services import AIPromptBuilder


class FakeAIAssistant:
    def __init__(self) -> None:
        self.context: AIContext | None = None
        self.prompt: str | None = None

    async def explain(
        self,
        context: AIContext,
        prompt: str,
    ) -> AIExplanation:
        self.context = context
        self.prompt = prompt
        return AIExplanation(
            summary="Assistive explanation",
            reasons=("Deterministic input",),
        )


@pytest.mark.asyncio
async def test_delegates_context_and_built_prompt() -> None:
    assistant = FakeAIAssistant()
    context = AIContext()
    use_case = ExplainDecisionUseCase(assistant, AIPromptBuilder())

    result = await use_case.execute(context)

    assert result.summary == "Assistive explanation"
    assert assistant.context is context
    assert assistant.prompt == AIPromptBuilder().build(context)


class FailingAIAssistant:
    async def explain(
        self,
        context: AIContext,
        prompt: str,
    ) -> AIExplanation:
        raise RuntimeError("assistant unavailable")


@pytest.mark.asyncio
async def test_propagates_assistant_errors() -> None:
    use_case = ExplainDecisionUseCase(FailingAIAssistant(), AIPromptBuilder())

    with pytest.raises(RuntimeError, match="assistant unavailable"):
        await use_case.execute(AIContext())
