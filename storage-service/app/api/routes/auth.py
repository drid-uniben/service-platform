from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.case_normalizer import SnakeCaseRoute
from app.db import get_db
from app.schemas.auth import CreateApiKeyRequest, CreateApiKeyResponse
from app.services.auth_service import create_api_key

router = APIRouter(prefix="/auth", tags=["auth"], route_class=SnakeCaseRoute)


@router.post("/keys", response_model=CreateApiKeyResponse, status_code=201)
def create_api_key_route(payload: CreateApiKeyRequest, db: Session = Depends(get_db)):
    return create_api_key(db, payload.account_name)
