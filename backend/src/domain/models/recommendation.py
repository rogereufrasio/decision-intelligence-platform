from pydantic import BaseModel, ConfigDict, Field

from src.domain.models.offer import Offer
from src.domain.models.preference_profile import PreferenceProfile
from src.domain.models.recommendation_score import RecommendationScore


class Recommendation(BaseModel):
    model_config = ConfigDict(frozen=True)

    offer: Offer
    score: RecommendationScore
    rank: int = Field(ge=1)
    profile: PreferenceProfile
    reasons: tuple[str, ...] = ()
