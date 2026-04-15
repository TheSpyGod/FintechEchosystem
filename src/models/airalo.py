from pydantic import BaseModel
from typing import Optional

class AiraloPackage(BaseModel):
    id: str
    name: str
    data_limit_gb: float
    validity_days: int
    price_usd: float

class AiraloOrderRequest(BaseModel):
    package_id: str
    quantity: int = 1

class AiraloOrderResponse(BaseModel):
    order_id: str
    status: str
    package_id: str
