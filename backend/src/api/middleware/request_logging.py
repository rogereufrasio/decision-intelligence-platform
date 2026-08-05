import logging
from time import perf_counter

from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from src.api.middleware.correlation_id import get_correlation_id
from src.core.metrics import MetricsCollector

logger = logging.getLogger("src.api.requests")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        metrics: MetricsCollector,
        observability_enabled: bool = True,
        metrics_enabled: bool = True,
    ) -> None:
        super().__init__(app)
        self._metrics = metrics
        self._observability_enabled = observability_enabled
        self._metrics_enabled = metrics_enabled

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        started_at = perf_counter()
        fields: dict[str, object] = {
            "correlation_id": get_correlation_id(),
            "method": request.method,
            "path": request.url.path,
        }
        if self._observability_enabled:
            logger.info(
                "request_started correlation_id=%s method=%s path=%s",
                fields["correlation_id"],
                fields["method"],
                fields["path"],
                extra=fields,
            )

        try:
            response = await call_next(request)
        except Exception:
            response = JSONResponse(
                status_code=500,
                content={"detail": "Internal server error"},
            )
            logger.exception(
                "request_failed correlation_id=%s method=%s path=%s",
                fields["correlation_id"],
                fields["method"],
                fields["path"],
                extra=fields,
            )

        elapsed_ms = max((perf_counter() - started_at) * 1000, 0.0)
        status_code = response.status_code
        completed_fields = {
            **fields,
            "status_code": status_code,
            "elapsed_ms": elapsed_ms,
        }
        if self._observability_enabled:
            logger.info(
                "request_completed correlation_id=%s method=%s path=%s "
                "status_code=%s elapsed_ms=%.3f",
                completed_fields["correlation_id"],
                completed_fields["method"],
                completed_fields["path"],
                completed_fields["status_code"],
                completed_fields["elapsed_ms"],
                extra=completed_fields,
            )
        if self._metrics_enabled:
            self._metrics.record(status_code, elapsed_ms)
        return response
