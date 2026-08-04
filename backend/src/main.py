from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.api.router import api_router
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