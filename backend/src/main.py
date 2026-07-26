import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.router import api_router
from src.core.config import get_settings
from src.core.logging import configure_logging
from src.shared.handlers import register_exception_handlers

configure_logging()

settings = get_settings()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting %s", settings.app_name)

    yield

    logger.info("Stopping %s", settings.app_name)


app = FastAPI(
    title=settings.app_name,
    description="Decision Intelligence Platform Backend",
    version=settings.app_version,
    lifespan=lifespan,
)

register_exception_handlers(app)

app.include_router(api_router)