import uuid
from sqlalchemy import text
from src.db.connection import engine

def create_tables():
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS packages (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                data_limit_gb REAL NOT NULL,
                validity_days INTEGER NOT NULL,
                price_usd REAL NOT NULL
            )
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS orders (
                id TEXT PRIMARY KEY,
                package_id TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (package_id) REFERENCES packages(id)
            )
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS payments (
                id TEXT PRIMARY KEY,
                order_id TEXT NOT NULL,
                amount INTEGER NOT NULL,
                currency TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (order_id) REFERENCES orders(id)
            )
        """))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS webhook_events (
                id TEXT PRIMARY KEY,
                event_type TEXT NOT NULL,
                payload TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """))

        conn.commit()
        print("Tables created.")

def seed_packages():
    packages = [
        (str(uuid.uuid4()), "Europe 1GB / 7 Days",  1.0,  7,  4.50),
        (str(uuid.uuid4()), "Europe 3GB / 30 Days", 3.0, 30, 11.00),
        (str(uuid.uuid4()), "Global 1GB / 7 Days",  1.0,  7,  8.00),
        (str(uuid.uuid4()), "Global 5GB / 30 Days", 5.0, 30, 22.00),
        (str(uuid.uuid4()), "USA 2GB / 14 Days",    2.0, 14,  9.50),
        (str(uuid.uuid4()), "Asia 3GB / 15 Days",   3.0, 15, 13.00),
    ]

    with engine.connect() as conn:
        for p in packages:
            conn.execute(text("""
                INSERT OR IGNORE INTO packages (id, name, data_limit_gb, validity_days, price_usd)
                VALUES (:id, :name, :data_limit_gb, :validity_days, :price_usd)
            """), {
                "id": p[0],
                "name": p[1],
                "data_limit_gb": p[2],
                "validity_days": p[3],
                "price_usd": p[4]
            })
        conn.commit()
        print(f"Seeded {len(packages)} packages.")

def seed_orders(package_ids):
    orders = [
        (str(uuid.uuid4()), package_ids[0], "completed"),
        (str(uuid.uuid4()), package_ids[1], "pending"),
        (str(uuid.uuid4()), package_ids[2], "failed"),
    ]

    with engine.connect() as conn:
        for o in orders:
            conn.execute(text("""
                INSERT OR IGNORE INTO orders (id, package_id, status)
                VALUES (:id, :package_id, :status)
            """), {
                "id": o[0],
                "package_id": o[1],
                "status": o[2]
            })
        conn.commit()
        print(f"Seeded {len(orders)} orders.")

    return [o[0] for o in orders]

def seed_payments(order_ids):
    payments = [
        (f"pi_{uuid.uuid4().hex[:24]}", order_ids[0], 450,  "usd", "succeeded"),
        (f"pi_{uuid.uuid4().hex[:24]}", order_ids[1], 1100, "usd", "requires_payment_method"),
        (f"pi_{uuid.uuid4().hex[:24]}", order_ids[2], 800,  "usd", "canceled"),
    ]

    with engine.connect() as conn:
        for p in payments:
            conn.execute(text("""
                INSERT OR IGNORE INTO payments (id, order_id, amount, currency, status)
                VALUES (:id, :order_id, :amount, :currency, :status)
            """), {
                "id": p[0],
                "order_id": p[1],
                "amount": p[2],
                "currency": p[3],
                "status": p[4]
            })
        conn.commit()
        print(f"Seeded {len(payments)} payments.")

def seed_webhook_events():
    events = [
        (str(uuid.uuid4()), "payment_intent.succeeded", '{"mock": true, "amount": 450}'),
        (str(uuid.uuid4()), "payment_intent.canceled",  '{"mock": true, "amount": 800}'),
    ]

    with engine.connect() as conn:
        for e in events:
            conn.execute(text("""
                INSERT OR IGNORE INTO webhook_events (id, event_type, payload)
                VALUES (:id, :event_type, :payload)
            """), {
                "id": e[0],
                "event_type": e[1],
                "payload": e[2]
            })
        conn.commit()
        print(f"Seeded {len(events)} webhook events.")

if __name__ == "__main__":
    print("Seeding database...")
    create_tables()
    seed_packages()

    package_ids = []
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id FROM packages LIMIT 3"))
        package_ids = [row[0] for row in result.fetchall()]

    order_ids = seed_orders(package_ids)
    seed_payments(order_ids)
    seed_webhook_events()
    print("Done.")
