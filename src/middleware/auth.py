import os
from dotenv import load_dotenv
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

load_dotenv()

USE_MOCK = os.getenv("USE_MOCK", "true") == "true"
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def authenticate(api_key: str = Security(api_key_header)):
    if USE_MOCK:
        return
    if api_key != os.getenv("GATEWAY_API_KEY"):
        raise HTTPException(status_code=403, detail="Unauthorized")
