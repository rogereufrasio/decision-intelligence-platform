from fastapi import APIRouter

from src.shared.responses import HealthResponse

router = APIRouter(prefix="/health", tags=["Health"])


@router.get(
    "",
    response_model=HealthResponse,
)
async def health() -> HealthResponse:
    return HealthResponse(
        status="healthy",
        service="decision-intelligence-platform",
        version="0.1.0",
    )