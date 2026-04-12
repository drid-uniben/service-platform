from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.dependencies.auth import require_api_key
from app.schemas import RegisterWebhookRequest, WebhookEndpointResponse
from app.services.webhook_service import register_endpoint

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("", response_model=WebhookEndpointResponse, status_code=201)
def register_webhook_route(
    payload: RegisterWebhookRequest,
    auth: tuple[str, str] = Depends(require_api_key),
    db: Session = Depends(get_db),
):
    account_id, _ = auth
    endpoint = register_endpoint(db, account_id, str(payload.url), payload.secret)

    return {
        "id": endpoint.id,
        "accountId": endpoint.account_id,
        "url": endpoint.url,
        "secret": endpoint.secret,
        "createdAt": endpoint.created_at,
    }
