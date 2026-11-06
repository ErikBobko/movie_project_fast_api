import os
import secrets

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from config import load_dotenv

load_dotenv()

# Získanie API kľúča z HTTP hlavičky X-API-Key
api_key_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=False,
)


def verify_api_key(api_key: str | None = Security(api_key_header)):
    # Načítanie nášho tajného kľúča z environment variables
    expected_key = os.getenv("SYNC_API_KEY")

    # Ak kľúč nie je nakonfigurovaný, synchronizácia sa nepovolí
    if not expected_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Sync API is not configured",
        )

    # Overenie kľúča, ktorý poslal používateľ
    if not api_key or not secrets.compare_digest(api_key, expected_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )