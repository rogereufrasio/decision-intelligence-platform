from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.router import api_router
from src.core.http import http_client


@asynccontextmanager
async def lifespan(app: FastAPI):

    yield

    await http_client.close()


app = FastAPI(
    title="Decision Intelligence Platform API",
    lifespan=lifespan,
)

app.include_router(
    api_router
)