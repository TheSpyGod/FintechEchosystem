from fastapi import APIRouter, Depends
from src.models.airalo import AiraloOrderRequest, AiraloOrderResponse, AiraloPackage
from src.services.airalo_service import get_packages, create_order, get_order_status
from src.middleware.auth import authenticate
from typing import List

router = APIRouter(prefix="/esims", tags=["Airalo"])

@router.get("/packages", response_model=List[AiraloPackage], dependencies=[Depends(authenticate)])
async def list_packages():
    return get_packages()

@router.post("/order", response_model=AiraloOrderResponse, dependencies=[Depends(authenticate)])
async def place_order(order: AiraloOrderRequest):
    return create_order(order)

@router.get("/order/{order_id}", response_model=AiraloOrderResponse, dependencies=[Depends(authenticate)])
async def order_status(order_id: str):
    return get_order_status(order_id)
