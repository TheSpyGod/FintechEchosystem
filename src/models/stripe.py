from pydantic import BaseModel

class PaymentIntentRequest(BaseModel):
    amount: int
    currency: str = "usd"
    order_id: str

class PaymentIntentResponse(BaseModel):
    intent_id: str
    client_secret: str
    status: str

class WebhookEvent(BaseModel):
    event_id: str
    event_type: str
    payload: dict
