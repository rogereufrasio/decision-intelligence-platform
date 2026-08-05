from decimal import Decimal

from pydantic import BaseModel, Field

from src.domain.models import Recommendation


class RecommendationOfferRequest(BaseModel):
    provider: str
    product_type: str
    price: Decimal
    currency: str
    metadata: dict[str, object] | None = None
    attributes: dict[str, object] | None = None


class RecommendationRequest(BaseModel):
    offers: list[RecommendationOfferRequest] = Field(default_factory=list)
    profile: str
    preferred_providers: list[str] | None = None


class RecommendationOfferResponse(BaseModel):
    provider: str
    product_type: str
    price: Decimal
    currency: str
    metadata: dict[str, object] | None = None
    attributes: dict[str, object] | None = None


class RecommendationScoreResponse(BaseModel):
    overall_score: Decimal
    price_score: Decimal
    duration_score: Decimal
    provider_score: Decimal


class RecommendationItemResponse(BaseModel):
    offer: RecommendationOfferResponse
    score: RecommendationScoreResponse
    rank: int
    profile: str
    reasons: list[str] = Field(default_factory=list)

    @classmethod
    def from_domain(
        cls,
        recommendation: Recommendation,
    ) -> "RecommendationItemResponse":
        return cls(
            offer=RecommendationOfferResponse(
                provider=recommendation.offer.provider,
                product_type=recommendation.offer.product_type,
                price=recommendation.offer.price,
                currency=recommendation.offer.currency,
                metadata=recommendation.offer.metadata,
                attributes=recommendation.offer.attributes,
            ),
            score=RecommendationScoreResponse(
                overall_score=recommendation.score.overall_score,
                price_score=recommendation.score.price_score,
                duration_score=recommendation.score.duration_score,
                provider_score=recommendation.score.provider_score,
            ),
            rank=recommendation.rank,
            profile=recommendation.profile.name.value,
            reasons=list(recommendation.reasons),
        )


class RecommendationsResponse(BaseModel):
    best_recommendation: RecommendationItemResponse | None = None
    recommendations: list[RecommendationItemResponse] = Field(
        default_factory=list
    )
    total: int
