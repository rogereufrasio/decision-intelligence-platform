from src.domain.models.decision_explanation import DecisionExplanation
from src.domain.models.decision_rule import RejectedRecommendation
from src.domain.models.preference_profile import PreferenceProfile
from src.domain.models.recommendation import Recommendation


class DecisionExplanationEngine:
    def explain(
        self,
        accepted: tuple[Recommendation, ...],
        rejected: tuple[RejectedRecommendation, ...],
        profile: PreferenceProfile,
    ) -> DecisionExplanation:
        rejected_count = len(rejected)
        warnings = (
            (f"Decision rules eliminated {rejected_count} option(s).",)
            if rejected_count
            else ()
        )
        if not accepted:
            return DecisionExplanation(
                summary="No recommendation satisfies the decision rules.",
                warnings=warnings,
                rejected_count=rejected_count,
                profile=profile.name,
            )

        selected = accepted[0]
        offer = selected.offer
        return DecisionExplanation(
            summary=(
                f"Selected {offer.provider} as the best recommendation "
                f"for the {profile.name.value} profile."
            ),
            reasons=selected.reasons,
            warnings=warnings,
            rejected_count=rejected_count,
            profile=profile.name,
            selected_offer=offer,
            selected_provider=offer.provider,
            selected_price=offer.price,
            selected_currency=offer.currency,
        )
