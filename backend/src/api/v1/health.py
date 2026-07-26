from fastapi import APIRouter

from src.shared.responses import HealthResponse
from src.shared.exceptions import DIPException

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

@router.get("/error")
async def error():

    raise DIPException(
        code="demo_error",
        message="This is a test exception.",
        status_code=400,
    )