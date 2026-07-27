from contextlib import asynccontextmanager

from fastapi import FastAPI

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

app.include_router(
    api_router
)