from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class AIExplanation(BaseModel):
    model_config = ConfigDict(frozen=True)

    summary: str
    reasons: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    confidence: Decimal | None = Field(default=None, ge=0, le=1)
    provider: str | None = None
    model: str | None = None
