import re

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from src.api.dependencies.travel import (
    get_export_search_snapshot_use_case,
)
from src.application.travel.export_search_snapshot import (
    ExportSearchSnapshotUseCase,
)


router = APIRouter(
    prefix="/search-history",
    tags=["Search History"],
)


@router.get(
    "/{search_id}/export",
)
async def export_search_snapshot(
    search_id: str,
    use_case: ExportSearchSnapshotUseCase | None = Depends(
        get_export_search_snapshot_use_case
    ),
) -> FileResponse:
    if not re.fullmatch(r"[A-Za-z0-9._-]+", search_id):
        raise HTTPException(
            status_code=422,
            detail={
                "code": "invalid_search_id",
                "message": "search_id contains invalid characters.",
            },
        )
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

    return FileResponse(
        path=output_path,
        media_type="application/vnd.apache.parquet",
        filename=f"search_{search_id}.parquet",
    )
