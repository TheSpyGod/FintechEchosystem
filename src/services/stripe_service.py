import os
import uuid
import hmac
import hashlib
from src.db.queries import execute

USE_MOCK = os.getenv("USE_MOCK", "true") == "true"
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")

def create_payment_intent(payment):
    if USE_MOCK:
        intent_id = f"pi_{uuid.uuid4().hex[:24]}"
        execute(
            "INSERT INTO payments (id, order_id, amount, currency, status) VALUES (:id, :order_id, :amount, :currency, :status)",
            {
                "id": intent_id,
                "order_id": payment.order_id,
                "amount": payment.amount,
                "currency": payment.currency,
                "status": "requires_payment_method"
            }
        )
        return {
            "intent_id": intent_id,
            "client_secret": f"{intent_id}_secret_{uuid.uuid4().hex[:16]}",
            "status": "requires_payment_method"
        }
    # real Stripe API call would go here

def verify_webhook(raw_body: bytes, signature: str):
    if USE_MOCK:
        execute(
            "INSERT INTO webhook_events (id, event_type, payload) VALUES (:id, :event_type, :payload)",
            {
                "id": str(uuid.uuid4()),
                "event_type": "mock.event",
                "payload": raw_body.decode("utf-8")
            }
        )
        return {"status": "received"}

    if not signature:
        raise ValueError("Missing Stripe signature")

    expected = hmac.new(
        STRIPE_WEBHOOK_SECRET.encode(),
        raw_body,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(expected, signature):
        raise ValueError("Invalid signature")

    return {"status": "verified"}
