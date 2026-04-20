from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from src.db.database import get_db, Transaction
from src.models.transaction import TransactionSchema, TransactionCreateRequest

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get("", response_model=List[TransactionSchema])
async def list_transactions(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Transaction))
    return result.scalars().all()


@router.post("", response_model=TransactionSchema, status_code=201)
async def create_transaction(body: TransactionCreateRequest, db: AsyncSession = Depends(get_db)):
    tx = Transaction(user_id=body.user_id, amount=body.amount, status=body.status)
    db.add(tx)
    await db.commit()
    await db.refresh(tx)
    return tx
