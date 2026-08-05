from src.application.ports.ai_assistant import AIAssistant
from src.domain.models.ai_context import AIContext
from src.domain.models.ai_explanation import AIExplanation
from src.domain.services.ai_prompt_builder import AIPromptBuilder


class ExplainDecisionUseCase:
    def __init__(
        self,
        assistant: AIAssistant,
        prompt_builder: AIPromptBuilder,
    ) -> None:
        self.assistant = assistant
        self.prompt_builder = prompt_builder

    async def execute(self, context: AIContext) -> AIExplanation:
        prompt = self.prompt_builder.build(context)
        return await self.assistant.explain(context, prompt)
