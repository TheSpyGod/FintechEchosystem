from fastapi import FastAPI
from src.routes.airalo import router as airalo_router
from src.routes.stripe import router as stripe_router
from src.routes.health import router as health_router

app = FastAPI(title="Fintech Gateway", version="1.0.0")

app.include_router(airalo_router, prefix="/api/v1")
app.include_router(stripe_router, prefix="/api/v1")
app.include_router(health_router, prefix="/api/v1")
