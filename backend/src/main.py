from fastapi import FastAPI

app = FastAPI(
    title="Decision Intelligence Platform API",
    version="0.1.0",
    description="Decision Intelligence Platform Backend",
)


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "decision-intelligence-platform",
    }