from decimal import Decimal

from src.domain.models import AIContext, AIExplanation


class TemplateAIAssistant:
    async def explain(
        self,
        context: AIContext,
        prompt: str,
    ) -> AIExplanation:
        del prompt
        summary = self._summary(context)
        reasons = self._reasons(context)
        warnings = self._warnings(context)
        has_context = bool(context.model_dump(exclude_none=True))
        return AIExplanation(
            summary=summary,
            reasons=reasons,
            warnings=warnings,
            confidence=Decimal("1") if has_context else Decimal("0"),
            provider="local",
            model="template",
        )

    @staticmethod
    def _summary(context: AIContext) -> str:
        if context.decision_explanation is not None:
            return context.decision_explanation.summary
        if context.decision_snapshot is not None:
            return context.decision_snapshot.explanation.summary
        if context.recommendation is not None:
            offer = context.recommendation.offer
            return (
                f"Recommendation from {offer.provider} at "
                f"{offer.price} {offer.currency}."
            )
        if context.price_intelligence is not None:
            price = context.price_intelligence
            if price.current_price is not None and price.currency is not None:
                return (
                    f"Current price is {price.current_price} "
                    f"{price.currency}; trend is {price.trend.value}."
                )
            return f"Price trend is {price.trend.value}."
        return "No decision context was provided."

    @classmethod
    def _reasons(cls, context: AIContext) -> tuple[str, ...]:
        values: list[str] = []
        if context.recommendation is not None:
            values.extend(context.recommendation.reasons)
        if context.decision_explanation is not None:
            values.extend(context.decision_explanation.reasons)
        if context.decision_snapshot is not None:
            values.extend(context.decision_snapshot.explanation.reasons)
        return cls._unique(values)

    @classmethod
    def _warnings(cls, context: AIContext) -> tuple[str, ...]:
        values: list[str] = []
        if context.decision_explanation is not None:
            values.extend(context.decision_explanation.warnings)
        if context.decision_snapshot is not None:
            values.extend(context.decision_snapshot.explanation.warnings)
        return cls._unique(values)

    @staticmethod
    def _unique(values: list[str]) -> tuple[str, ...]:
        return tuple(dict.fromkeys(values))
