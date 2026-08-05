from fastapi import APIRouter, Depends, HTTPException

from src.api.dependencies.travel import get_analyze_price_history_use_case
from src.api.schemas.price_intelligence_schema import (
    PriceIntelligenceResponse,
)
from src.application.travel.analyze_price_history import (
    AnalyzePriceHistoryUseCase,
)


router = APIRouter(
    prefix="/price-intelligence",
    tags=["Price Intelligence"],
)


@router.get(
    "/{search_id}",
    response_model=PriceIntelligenceResponse,
)
async def analyze_price_history(
    search_id: str,
    limit: int = 20,
    use_case: AnalyzePriceHistoryUseCase | None = Depends(
        get_analyze_price_history_use_case
    ),
) -> PriceIntelligenceResponse:
    if use_case is None:
        raise HTTPException(
            status_code=503,
            detail={
                "code": "search_persistence_disabled",
                "message": "Search persistence is disabled.",
            },
        )

    try:
        result = await use_case.execute(search_id, limit)
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail={
                "code": "invalid_history_limit",
                "message": str(exc),
            },
        ) from exc

    if result is None:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "search_snapshot_not_found",
                "message": f"Search snapshot '{search_id}' was not found.",
            },
        )

    return PriceIntelligenceResponse.model_validate(result)
