from decimal import Decimal

from pydantic import BaseModel, Field

from src.domain.models import AIContext, AIExplanation


class AIExplanationRequest(BaseModel):
    context: AIContext
    correlation_id: str | None = None


class AIExplanationResponse(BaseModel):
    summary: str
    reasons: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    confidence: Decimal | None = None
    provider: str | None = None
    model: str | None = None
    correlation_id: str | None = None

    @classmethod
    def from_domain(
        cls,
        explanation: AIExplanation,
        correlation_id: str | None,
    ) -> "AIExplanationResponse":
        return cls(
            summary=explanation.summary,
            reasons=list(explanation.reasons),
            warnings=list(explanation.warnings),
            confidence=explanation.confidence,
            provider=explanation.provider,
            model=explanation.model,
            correlation_id=correlation_id,
        )
