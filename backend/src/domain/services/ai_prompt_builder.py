import json

from src.domain.models.ai_context import AIContext


class AIPromptBuilder:
    def build(self, context: AIContext) -> str:
        payload = context.model_dump(mode="json", exclude_none=True)
        serialized_context = json.dumps(
            payload,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
        return (
            "Explain the decision using only the supplied context. "
            "Do not invent facts. Return a concise summary, reasons, and "
            f"warnings. Context: {serialized_context}"
        )
