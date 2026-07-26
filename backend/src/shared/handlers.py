import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.shared.error_response import ErrorResponse
from src.shared.exceptions import DIPException

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(DIPException)
    async def dip_exception_handler(
        request: Request,
        exc: DIPException,
    ):
        logger.warning(
            "%s - %s",
            exc.code,
            exc.message,
        )

        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                code=exc.code,
                message=exc.message,
            ).model_dump(),
        )

    @app.exception_handler(Exception)
    async def unexpected_exception_handler(
        request: Request,
        exc: Exception,
    ):
        logger.exception(exc)

        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                code="internal_server_error",
                message="Internal server error.",
            ).model_dump(),
        )