import os
from dotenv import load_dotenv
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

load_dotenv()

api_key_header = APIKeyHeader(name="X-API-Key")

def authenticate(api_key: str = Security(api_key_header)):
    if api_key != os.getenv("GATEWAY_API_KEY"):
        raise HTTPException(status_code=403, detail="Unauthorized")
