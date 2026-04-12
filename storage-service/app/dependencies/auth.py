from fastapi import Depends, Header, HTTPException, Request
from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.db import get_db
from app.rate_limiter import InMemoryRateLimiter
from app.services.auth_service import validate_api_key

rate_limiter = InMemoryRateLimiter()


def require_api_key(
    request: Request,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
    x_api_key: str | None = Header(default=None),
) -> tuple[str, str]:
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing x-api-key header.")

    api_key = validate_api_key(db, x_api_key)
    if not api_key:
        raise HTTPException(status_code=401, detail="Invalid API key.")

    if not rate_limiter.is_allowed(api_key.id, settings.api_key_rate_limit_per_minute):
        raise HTTPException(status_code=429, detail="Rate limit exceeded for API key.")

    request.state.account_id = api_key.account_id
    request.state.api_key_id = api_key.id
    return api_key.account_id, api_key.id
