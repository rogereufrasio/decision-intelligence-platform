from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from src.api.schemas.recommendation_schema import (
    RecommendationItemResponse,
    RecommendationOfferResponse,
)
from src.domain.models import DecisionSnapshot


class RejectedDecisionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    recommendation: RecommendationItemResponse
    reasons: tuple[str, ...] = ()


class DecisionExplanationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    summary: str
    reasons: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    rejected_count: int
    profile: str
    selected_offer: RecommendationOfferResponse | None = None
    selected_provider: str | None = None
    selected_price: Decimal | None = None
    selected_currency: str | None = None


class DecisionSnapshotResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    decision_id: str
    search_id: str | None = None
    created_at: datetime
    profile: str
    accepted: tuple[RecommendationItemResponse, ...] = ()
    rejected: tuple[RejectedDecisionResponse, ...] = ()
    explanation: DecisionExplanationResponse
    selected_offer: RecommendationOfferResponse | None = None
    schema_version: str
    correlation_id: str | None = None

    @classmethod
    def from_domain(cls, snapshot: DecisionSnapshot) -> "DecisionSnapshotResponse":
        return cls(
            decision_id=snapshot.decision_id,
            search_id=snapshot.search_id,
            created_at=snapshot.created_at,
            profile=snapshot.profile.value,
            accepted=tuple(
                RecommendationItemResponse.from_domain(item)
                for item in snapshot.accepted
            ),
            rejected=tuple(
                RejectedDecisionResponse(
                    recommendation=RecommendationItemResponse.from_domain(
                        item.recommendation
                    ),
                    reasons=item.reasons,
                )
                for item in snapshot.rejected
            ),
            explanation=DecisionExplanationResponse.model_validate(
                snapshot.explanation.model_dump()
            ),
            selected_offer=(
                RecommendationOfferResponse.model_validate(
                    snapshot.selected_offer.model_dump()
                )
                if snapshot.selected_offer is not None
                else None
            ),
            schema_version=snapshot.schema_version,
            correlation_id=snapshot.correlation_id,
        )


class DecisionHistoryResponse(BaseModel):
    items: list[DecisionSnapshotResponse] = Field(default_factory=list)
    total: int
