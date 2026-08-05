from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.domain.models.decision_explanation import DecisionExplanation
from src.domain.models.decision_rule import RejectedRecommendation
from src.domain.models.offer import Offer
from src.domain.models.preference_profile import PreferenceProfileName
from src.domain.models.recommendation import Recommendation


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class DecisionSnapshot(BaseModel):
    model_config = ConfigDict(frozen=True)

    decision_id: str
    search_id: str | None = None
    created_at: datetime = Field(default_factory=utc_now)
    profile: PreferenceProfileName
    accepted: tuple[Recommendation, ...] = ()
    rejected: tuple[RejectedRecommendation, ...] = ()
    explanation: DecisionExplanation
    selected_offer: Offer | None = None
    schema_version: str = "1.0"
    correlation_id: str | None = None

    @field_validator("created_at")
    @classmethod
    def ensure_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("created_at must be timezone-aware")
        return value.astimezone(timezone.utc)
