from src.domain.models import (
    DecisionRule,
    PreferenceProfile,
    Recommendation,
    RecommendationEvaluation,
)
from src.domain.services import DecisionExplanationEngine, RuleEngine


class EvaluateRecommendationsUseCase:
    def __init__(
        self,
        rule_engine: RuleEngine,
        explanation_engine: DecisionExplanationEngine,
    ) -> None:
        self.rule_engine = rule_engine
        self.explanation_engine = explanation_engine

    def execute(
        self,
        recommendations: list[Recommendation],
        rules: list[DecisionRule],
        profile: PreferenceProfile,
    ) -> RecommendationEvaluation:
        evaluation = self.rule_engine.evaluate(recommendations, rules)
        explanation = self.explanation_engine.explain(
            evaluation.accepted,
            evaluation.rejected,
            profile,
        )
        return RecommendationEvaluation(
            accepted=evaluation.accepted,
            rejected=evaluation.rejected,
            explanation=explanation,
        )
