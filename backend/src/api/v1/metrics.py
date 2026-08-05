from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from src.core.config import Settings, get_settings
from src.core.metrics import MetricsCollector, metrics_collector

router = APIRouter(prefix="/metrics", tags=["Metrics"])


class MetricsResponse(BaseModel):
    total_requests: int
    requests_by_status: dict[str, int] = Field(default_factory=dict)
    total_errors: int
    average_response_time_ms: float


def get_metrics_collector() -> MetricsCollector:
    return metrics_collector


@router.get("", response_model=MetricsResponse)
async def get_metrics(
    settings: Settings = Depends(get_settings),
    collector: MetricsCollector = Depends(get_metrics_collector),
) -> MetricsResponse:
    if not settings.metrics_enabled:
        raise HTTPException(
            status_code=503,
            detail={
                "code": "metrics_disabled",
                "message": "Metrics collection is disabled.",
            },
        )
    return MetricsResponse.model_validate(collector.snapshot())
