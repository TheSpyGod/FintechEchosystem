from fastapi import APIRouter, Depends, Request, HTTPException
from src.models.stripe import PaymentIntentRequest, PaymentIntentResponse, WebhookEvent
from src.services.stripe_service import create_payment_intent, verify_webhook
from src.middleware.auth import authenticate

router = APIRouter(prefix="/payments", tags=["Stripe"])

@router.post("/intent", response_model=PaymentIntentResponse, dependencies=[Depends(authenticate)])
async def payment_intent(payment: PaymentIntentRequest):
    return create_payment_intent(payment)

@router.post("/webhook")
async def webhook(request: Request):
    raw_body = await request.body()
    signature = request.headers.get("stripe-signature")
    return verify_webhook(raw_body, signature)
