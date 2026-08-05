from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class RecommendationScore(BaseModel):
    model_config = ConfigDict(frozen=True)

    overall_score: Decimal = Field(ge=0, le=100)
    price_score: Decimal = Field(ge=0, le=100)
    duration_score: Decimal = Field(ge=0, le=100)
    provider_score: Decimal = Field(ge=0, le=100)
