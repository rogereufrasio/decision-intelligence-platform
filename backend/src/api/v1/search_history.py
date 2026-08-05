from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from src.api.dependencies.travel import (
    get_search_history_use_case,
    get_search_snapshot_use_case,
)
from src.api.schemas.search_history_schema import (
    SearchHistoryResponse,
    SearchSnapshotResponse,
)
from src.application.travel.get_search_history import (
    GetSearchHistoryUseCase,
)
from src.application.travel.get_search_snapshot import (
    GetSearchSnapshotUseCase,
)


router = APIRouter(
    prefix="/search-history",
    tags=["Search History"],
)


def persistence_disabled_error() -> HTTPException:
    return HTTPException(
        status_code=503,
        detail={
            "code": "search_persistence_disabled",
            "message": "Search persistence is disabled.",
        },
    )


@router.get(
    "",
    response_model=SearchHistoryResponse,
)
async def get_search_history(
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    use_case: GetSearchHistoryUseCase | None = Depends(
        get_search_history_use_case
    ),
) -> SearchHistoryResponse:
    if use_case is None:
        raise persistence_disabled_error()

    snapshots = await use_case.execute(limit)
    items = [
        SearchSnapshotResponse.model_validate(snapshot)
        for snapshot in snapshots
    ]
    return SearchHistoryResponse(
        items=items,
        total=len(items),
    )


@router.get(
    "/{search_id}",
    response_model=SearchSnapshotResponse,
)
async def get_search_snapshot(
    search_id: str,
    use_case: GetSearchSnapshotUseCase | None = Depends(
        get_search_snapshot_use_case
    ),
) -> SearchSnapshotResponse:
    if use_case is None:
        raise persistence_disabled_error()

    snapshot = await use_case.execute(search_id)
    if snapshot is None:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "search_snapshot_not_found",
                "message": f"Search snapshot '{search_id}' was not found.",
            },
        )

    return SearchSnapshotResponse.model_validate(snapshot)
