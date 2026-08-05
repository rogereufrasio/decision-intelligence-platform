from typing import Protocol, runtime_checkable

from src.domain.models.ai_context import AIContext
from src.domain.models.ai_explanation import AIExplanation


@runtime_checkable
class AIAssistant(Protocol):
    async def explain(
        self,
        context: AIContext,
        prompt: str,
    ) -> AIExplanation: ...
