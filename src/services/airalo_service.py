import os
import uuid
from src.db.queries import execute

USE_MOCK = os.getenv("USE_MOCK", "true") == "true"

def get_packages():
    if USE_MOCK:
        result = execute("SELECT * FROM packages")
        return [
            {
                "id": str(row[0]),
                "name": row[1],
                "data_limit_gb": row[2],
                "validity_days": row[3],
                "price_usd": row[4]
            }
            for row in result
        ]
    # real Airalo API call would go here

def create_order(order):
    if USE_MOCK:
        order_id = str(uuid.uuid4())
        execute(
            "INSERT INTO orders (id, package_id, status) VALUES (:id, :package_id, :status)",
            {"id": order_id, "package_id": order.package_id, "status": "pending"}
        )
        return {
            "order_id": order_id,
            "status": "pending",
            "package_id": order.package_id
        }
    # real Airalo API call would go here

def get_order_status(order_id: str):
    if USE_MOCK:
        result = execute(
            "SELECT * FROM orders WHERE id = :id",
            {"id": order_id}
        )
        if not result:
            raise ValueError(f"Order {order_id} not found")
        row = result[0]
        return {
            "order_id": str(row[0]),
            "status": row[2],
            "package_id": str(row[1])
        }
    # real Airalo API call would go here
