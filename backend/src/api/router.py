from fastapi import APIRouter

from src.api.v1.health import router as health_router
from src.shared.exceptions import DIPException

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(health_router)

