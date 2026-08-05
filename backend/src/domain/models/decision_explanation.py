from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from src.domain.models.decision_rule import RejectedRecommendation
from src.domain.models.offer import Offer
from src.domain.models.preference_profile import PreferenceProfileName
from src.domain.models.recommendation import Recommendation


class DecisionExplanation(BaseModel):
    model_config = ConfigDict(frozen=True)

    summary: str
    reasons: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    rejected_count: int
    profile: PreferenceProfileName
    selected_offer: Offer | None = None
    selected_provider: str | None = None
    selected_price: Decimal | None = None
    selected_currency: str | None = None


class RecommendationEvaluation(BaseModel):
    model_config = ConfigDict(frozen=True)

    accepted: tuple[Recommendation, ...] = ()
    rejected: tuple[RejectedRecommendation, ...] = ()
    explanation: DecisionExplanation
