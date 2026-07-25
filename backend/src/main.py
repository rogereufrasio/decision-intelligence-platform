from fastapi import FastAPI

from src.api.router import api_router

app = FastAPI(
    title="Decision Intelligence Platform API",
    description="Decision Intelligence Platform Backend",
    version="0.1.0",
)

app.include_router(api_router)