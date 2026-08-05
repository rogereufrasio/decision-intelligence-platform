from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.api.router import api_router
from src.api.middleware.correlation_id import CorrelationIdMiddleware
from src.api.middleware.request_logging import RequestLoggingMiddleware
from src.api.middleware.security_headers import SecurityHeadersMiddleware
from src.core.config import get_settings
from src.core.metrics import metrics_collector
from src.infrastructure.container import Container


container = Container()


@asynccontextmanager
async def lifespan(app: FastAPI):

    yield

    await container.close()


app = FastAPI(
    title="Decision Intelligence Platform API",
    lifespan=lifespan,
)

settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        origin.strip()
        for origin in settings.cors_allowed_origins.split(",")
        if origin.strip()
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "X-Correlation-ID", "X-Travel-Provider"],
)
app.add_middleware(
    RequestLoggingMiddleware,
    metrics=metrics_collector,
    observability_enabled=settings.observability_enabled,
    metrics_enabled=settings.metrics_enabled,
)
app.add_middleware(CorrelationIdMiddleware)
app.add_middleware(
    SecurityHeadersMiddleware,
    enabled=settings.security_headers_enabled,
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={
            "detail": exc.errors(),
            "body": exc.body,
        },
    )


app.include_router(
    api_router
)
