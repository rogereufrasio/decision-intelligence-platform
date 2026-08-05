from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.core.readiness import ReadinessService
from src.infrastructure.container import Container

router = APIRouter(prefix="/readiness", tags=["Readiness"])


class ReadinessCheckResponse(BaseModel):
    name: str
    status: str
    message: str


class ReadinessResponse(BaseModel):
    status: str
    checks: list[ReadinessCheckResponse]


def get_readiness_service() -> ReadinessService:
    return Container().get_readiness_service()


@router.get("", response_model=ReadinessResponse)
async def readiness(
    service: ReadinessService = Depends(get_readiness_service),
) -> ReadinessResponse | JSONResponse:
    result = service.evaluate()
    payload = ReadinessResponse(
        status="ready" if result.ready else "not_ready",
        checks=[
            ReadinessCheckResponse(
                name=check.name,
                status=check.status,
                message=check.message,
            )
            for check in result.checks
        ],
    )
    if not result.ready:
        return JSONResponse(
            status_code=503,
            content=payload.model_dump(mode="json"),
        )
    return payload
