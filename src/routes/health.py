import httpx
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from src.db.database import get_db
from src.config import settings

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
async def health(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception as e:
        db_status = f"error: {str(e)}"

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                "https://api.stripe.com/v1/customers",
                headers={"Authorization": f"Bearer {settings.stripe_secret_key_sandbox}"},
                params={"limit": 1},
                timeout=5.0,
            )
        stripe_status = "ok" if resp.status_code < 500 else f"error: {resp.status_code}"
    except Exception as e:
        stripe_status = f"error: {str(e)}"

    overall = "ok" if db_status == "ok" and stripe_status == "ok" else "degraded"
    return {
        "status": overall,
        "database": db_status,
        "stripe": stripe_status,
    }
