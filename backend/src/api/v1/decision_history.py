from fastapi import APIRouter, Depends, HTTPException

from src.api.dependencies.travel import get_decision_history_use_case
from src.api.schemas.decision_history_schema import (
    DecisionHistoryResponse,
    DecisionSnapshotResponse,
)
from src.application.travel.get_decision_history import GetDecisionHistoryUseCase

router = APIRouter(prefix="/decision-history", tags=["Decision History"])


@router.get("", response_model=DecisionHistoryResponse)
async def get_decision_history(
    limit: int = 20,
    use_case: GetDecisionHistoryUseCase | None = Depends(
        get_decision_history_use_case
    ),
) -> DecisionHistoryResponse:
    if not 1 <= limit <= 100:
        raise HTTPException(
            status_code=422,
            detail={
                "code": "invalid_history_limit",
                "message": "limit must be between 1 and 100",
            },
        )
    if use_case is None:
        raise HTTPException(status_code=503, detail={
            "code": "decision_persistence_disabled",
            "message": "Decision persistence is disabled.",
        })
    try:
        snapshots = await use_case.execute(limit)
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail={"code": "invalid_history_limit", "message": str(exc)},
        ) from exc
    items = [DecisionSnapshotResponse.from_domain(item) for item in snapshots]
    return DecisionHistoryResponse(items=items, total=len(items))
