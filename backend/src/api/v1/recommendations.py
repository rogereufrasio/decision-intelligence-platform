from fastapi import APIRouter, Depends, HTTPException

from src.api.dependencies.travel import get_recommend_travel_offers_use_case
from src.api.schemas.recommendation_schema import (
    RecommendationRequest,
    RecommendationItemResponse,
    RecommendationsResponse,
)
from src.application.travel.recommend_travel_offers import (
    RecommendTravelOffersUseCase,
)
from src.domain.models import Offer, PreferenceProfile, PreferenceProfileName


router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)


@router.post(
    "",
    response_model=RecommendationsResponse,
)
async def recommend_travel_offers(
    request: RecommendationRequest,
    use_case: RecommendTravelOffersUseCase = Depends(
        get_recommend_travel_offers_use_case
    ),
) -> RecommendationsResponse:
    try:
        profile_name = PreferenceProfileName(request.profile)
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail={
                "code": "invalid_preference_profile",
                "message": f"Unknown preference profile: {request.profile}",
            },
        ) from exc

    profile = _build_profile(profile_name)
    offers = [
        Offer.model_validate(offer.model_dump())
        for offer in request.offers
    ]
    recommendations = use_case.execute(
        offers=offers,
        profile=profile,
        preferred_providers=request.preferred_providers,
    )
    items = [
        RecommendationItemResponse.from_domain(recommendation)
        for recommendation in recommendations[:5]
    ]

    return RecommendationsResponse(
        best_recommendation=items[0] if items else None,
        recommendations=items,
        total=len(items),
    )


def _build_profile(name: PreferenceProfileName) -> PreferenceProfile:
    if name is PreferenceProfileName.CHEAPEST:
        return PreferenceProfile.cheapest()
    if name is PreferenceProfileName.FASTEST:
        return PreferenceProfile.fastest()
    if name is PreferenceProfileName.PREMIUM:
        return PreferenceProfile.premium()
    return PreferenceProfile.balanced()
