from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.db.database import engine, Base
from src.routes.airalo import router as airalo_router
from src.routes.stripe import router as stripe_router
from src.routes.health import router as health_router
from src.routes.transactions import router as transactions_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="Fintech Gateway",
    version="1.0.0",
    description=(
        "Asynchronous FinTech boilerplate integrating Stripe payments and Airalo eSIM services. "
        "FastAPI leverages asyncio's event loop so that calls to Stripe and Airalo are "
        "non-blocking: both HTTP requests can be dispatched concurrently via "
        "`asyncio.gather(stripe_task, airalo_task)` and the handler resumes only when both "
        "resolve, eliminating serial wait time and keeping the server thread-free."
    ),
    lifespan=lifespan,
)

app.include_router(airalo_router, prefix="/api/v1")
app.include_router(stripe_router, prefix="/api/v1")
app.include_router(health_router, prefix="/api/v1")
app.include_router(transactions_router, prefix="/api/v1")
