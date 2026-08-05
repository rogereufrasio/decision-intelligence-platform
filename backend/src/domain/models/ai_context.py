from pydantic import BaseModel, ConfigDict

from src.domain.models.decision_explanation import DecisionExplanation
from src.domain.models.decision_snapshot import DecisionSnapshot
from src.domain.models.price_intelligence import PriceIntelligence
from src.domain.models.recommendation import Recommendation


class AIContext(BaseModel):
    model_config = ConfigDict(frozen=True)

    recommendation: Recommendation | None = None
    decision_explanation: DecisionExplanation | None = None
    decision_snapshot: DecisionSnapshot | None = None
    price_intelligence: PriceIntelligence | None = None
