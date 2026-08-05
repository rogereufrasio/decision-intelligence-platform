from fastapi import APIRouter

from src.api.v1.ai_explanations import router as ai_explanations_router
from src.api.v1.decision_history import router as decision_history_router
from src.api.v1.health import router as health_router
from src.api.v1.metrics import router as metrics_router
from src.api.v1.flights import router as flights_router
from src.api.v1.price_intelligence import router as price_intelligence_router
from src.api.v1.recommendations import router as recommendations_router
from src.api.v1.search_comparison import router as search_comparison_router
from src.api.v1.search_export import router as search_export_router
from src.api.v1.search_history import router as search_history_router
from src.api.v1.travel import router as travel_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(health_router)
api_router.include_router(travel_router)
api_router.include_router(flights_router)
api_router.include_router(search_history_router)
api_router.include_router(search_comparison_router)
api_router.include_router(search_export_router)
api_router.include_router(recommendations_router)
api_router.include_router(price_intelligence_router)
api_router.include_router(decision_history_router)
api_router.include_router(ai_explanations_router)
api_router.include_router(metrics_router)
