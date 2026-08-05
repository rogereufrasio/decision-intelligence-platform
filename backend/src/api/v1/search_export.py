from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from src.api.dependencies.travel import (
    get_export_search_snapshot_use_case,
)
from src.application.travel.export_search_snapshot import (
    ExportSearchSnapshotUseCase,
)


class SearchExportResponse(BaseModel):
    search_id: str
    file: str
    format: str


router = APIRouter(
    prefix="/search-history",
    tags=["Search History"],
)


@router.get(
    "/{search_id}/export",
    response_model=SearchExportResponse,
)
async def export_search_snapshot(
    search_id: str,
    use_case: ExportSearchSnapshotUseCase | None = Depends(
        get_export_search_snapshot_use_case
    ),
) -> SearchExportResponse:
    if use_case is None:
        raise HTTPException(
            status_code=503,
            detail={
                "code": "search_persistence_disabled",
                "message": "Search persistence is disabled.",
            },
        )

    output_path = await use_case.execute(search_id)
    if output_path is None:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "search_snapshot_not_found",
                "message": f"Search snapshot '{search_id}' was not found.",
            },
        )

    return SearchExportResponse(
        search_id=search_id,
        file=str(output_path),
        format="parquet",
    )
