from decimal import Decimal, InvalidOperation

from src.domain.models.decision_rule import (
    DecisionRule,
    RejectedRecommendation,
    RuleEvaluationResult,
    RuleOperator,
    RuleScalar,
    RuleValue,
)
from src.domain.models.recommendation import Recommendation


class RuleEngine:
    SUPPORTED_FIELDS = {
        "offer.provider",
        "offer.price",
        "offer.currency",
        "offer.product_type",
        "offer.attributes.total_duration_minutes",
        "offer.attributes.stops",
        "recommendation.score.overall_score",
    }

    def evaluate(
        self,
        recommendations: list[Recommendation],
        rules: list[DecisionRule],
    ) -> RuleEvaluationResult:
        enabled_rules = [rule for rule in rules if rule.enabled]
        accepted: list[Recommendation] = []
        rejected: list[RejectedRecommendation] = []

        for recommendation in recommendations:
            reasons = tuple(
                rule.reason
                for rule in enabled_rules
                if not self._matches(recommendation, rule)
            )
            if reasons:
                rejected.append(
                    RejectedRecommendation(
                        recommendation=recommendation,
                        reasons=reasons,
                    )
                )
            else:
                accepted.append(recommendation)

        return RuleEvaluationResult(
            accepted=tuple(accepted),
            rejected=tuple(rejected),
        )

    def _matches(
        self,
        recommendation: Recommendation,
        rule: DecisionRule,
    ) -> bool:
        actual = self._resolve_field(recommendation, rule.field)
        if actual is None:
            return False

        expected = rule.value
        try:
            if rule.operator == RuleOperator.EQUALS:
                return self._equal(actual, expected)
            if rule.operator == RuleOperator.NOT_EQUALS:
                return not self._equal(actual, expected)
            if rule.operator == RuleOperator.CONTAINS:
                return self._contains(actual, expected)
            if rule.operator == RuleOperator.IN:
                return self._in(actual, expected)

            left, right = self._comparable_values(actual, expected)
            if rule.operator == RuleOperator.LESS_THAN:
                return left < right
            if rule.operator == RuleOperator.LESS_THAN_OR_EQUAL:
                return left <= right
            if rule.operator == RuleOperator.GREATER_THAN:
                return left > right
            if rule.operator == RuleOperator.GREATER_THAN_OR_EQUAL:
                return left >= right
        except (InvalidOperation, TypeError, ValueError):
            return False
        return False

    def _resolve_field(
        self,
        recommendation: Recommendation,
        field: str,
    ) -> RuleScalar | None:
        if field not in self.SUPPORTED_FIELDS:
            return None
        if field == "recommendation.score.overall_score":
            return recommendation.score.overall_score

        path = field.removeprefix("offer.")
        if path.startswith("attributes."):
            attributes = recommendation.offer.attributes or {}
            value = attributes.get(path.removeprefix("attributes."))
        else:
            value = getattr(recommendation.offer, path, None)

        if isinstance(value, (str, Decimal, int, bool)):
            return value
        return None

    @classmethod
    def _equal(cls, actual: RuleScalar, expected: RuleValue) -> bool:
        if isinstance(expected, tuple):
            return False
        try:
            left, right = cls._comparable_values(actual, expected)
            return left == right
        except (InvalidOperation, TypeError, ValueError):
            return actual == expected

    @staticmethod
    def _contains(actual: RuleScalar, expected: RuleValue) -> bool:
        if isinstance(expected, tuple):
            return False
        if isinstance(actual, str):
            return str(expected) in actual
        return False

    @classmethod
    def _in(cls, actual: RuleScalar, expected: RuleValue) -> bool:
        if not isinstance(expected, tuple):
            return False
        return any(cls._equal(actual, item) for item in expected)

    @staticmethod
    def _comparable_values(
        actual: RuleScalar,
        expected: RuleValue,
    ) -> tuple[Decimal, Decimal] | tuple[str, str]:
        if isinstance(expected, tuple):
            raise TypeError("collection is not an ordered scalar")
        if isinstance(actual, (Decimal, int)) and not isinstance(actual, bool):
            return Decimal(str(actual)), Decimal(str(expected))
        return str(actual), str(expected)
