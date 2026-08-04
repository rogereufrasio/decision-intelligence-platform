from fastapi import APIRouter

from src.api.v1.health import router as health_router
from src.api.v1.flights import router as flights_router
from src.api.v1.travel import router as travel_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(health_router)
api_router.include_router(travel_router)
api_router.include_router(flights_router)