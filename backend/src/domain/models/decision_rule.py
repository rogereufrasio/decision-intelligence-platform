from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict

from src.domain.models.recommendation import Recommendation


class RuleOperator(str, Enum):
    EQUALS = "equals"
    NOT_EQUALS = "not_equals"
    LESS_THAN = "less_than"
    LESS_THAN_OR_EQUAL = "less_than_or_equal"
    GREATER_THAN = "greater_than"
    GREATER_THAN_OR_EQUAL = "greater_than_or_equal"
    CONTAINS = "contains"
    IN = "in"


RuleScalar = str | Decimal | int | bool
RuleValue = RuleScalar | tuple[RuleScalar, ...]


class DecisionRule(BaseModel):
    model_config = ConfigDict(frozen=True)

    rule_id: str
    rule_type: str
    field: str
    operator: RuleOperator
    value: RuleValue
    reason: str
    enabled: bool = True


class RejectedRecommendation(BaseModel):
    model_config = ConfigDict(frozen=True)

    recommendation: Recommendation
    reasons: tuple[str, ...]


class RuleEvaluationResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    accepted: tuple[Recommendation, ...] = ()
    rejected: tuple[RejectedRecommendation, ...] = ()
