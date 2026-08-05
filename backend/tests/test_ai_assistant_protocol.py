from src.application.ports import AIAssistant
from src.domain.models import AIContext, AIExplanation


class CompatibleAssistant:
    async def explain(
        self,
        context: AIContext,
        prompt: str,
    ) -> AIExplanation:
        return AIExplanation(summary="Compatible")


class IncompatibleAssistant:
    pass


def test_runtime_protocol_accepts_compatible_assistant() -> None:
    assert isinstance(CompatibleAssistant(), AIAssistant)


def test_runtime_protocol_rejects_incompatible_assistant() -> None:
    assert not isinstance(IncompatibleAssistant(), AIAssistant)
