from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from src.api.dependencies.travel import (
    get_compare_search_snapshots_use_case,
)
from src.api.schemas.search_comparison_schema import (
    SearchComparisonResponse,
)
from src.application.travel.compare_search_snapshots import (
    CompareSearchSnapshotsUseCase,
    NoComparableCurrencyError,
)


router = APIRouter(
    prefix="/search-comparison",
    tags=["Search Comparison"],
)


@router.get(
    "",
    response_model=SearchComparisonResponse,
)
async def compare_search_snapshots(
    base_search_id: Annotated[str, Query(min_length=1)],
    target_search_id: Annotated[str, Query(min_length=1)],
    use_case: CompareSearchSnapshotsUseCase | None = Depends(
        get_compare_search_snapshots_use_case
    ),
) -> SearchComparisonResponse:
    if use_case is None:
        raise HTTPException(
            status_code=503,
            detail={
                "code": "search_persistence_disabled",
                "message": "Search persistence is disabled.",
            },
        )

    try:
        comparison = await use_case.execute(
            base_search_id,
            target_search_id,
        )
    except NoComparableCurrencyError as exc:
        raise HTTPException(
            status_code=409,
            detail={
                "code": "no_comparable_currency",
                "message": str(exc),
            },
        ) from exc

    if comparison is None:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "search_snapshot_not_found",
                "message": "One or both search snapshots were not found.",
            },
        )

    return SearchComparisonResponse.model_validate(comparison)
