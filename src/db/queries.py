from sqlalchemy import text
from src.db.connection import engine

def execute(query: str, params: dict = {}):
    with engine.connect() as conn:
        result = conn.execute(text(query), params)
        conn.commit()
        return result.fetchall()
