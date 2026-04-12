import json
from datetime import datetime, timezone

import httpx
from sqlalchemy.orm import Session

from app.models import WebhookEndpoint
from app.security import hmac_sha256


def register_endpoint(db: Session, account_id: str, url: str, secret: str) -> WebhookEndpoint:
    endpoint = WebhookEndpoint(account_id=account_id, url=url, secret=secret)
    db.add(endpoint)
    db.commit()
    db.refresh(endpoint)
    return endpoint


def emit_storage_event(db: Session, account_id: str, payload: dict) -> None:
    endpoints = db.query(WebhookEndpoint).filter(WebhookEndpoint.account_id == account_id).all()
    if not endpoints:
        return

    body = json.dumps({**payload, "timestamp": datetime.now(timezone.utc).isoformat()})
    with httpx.Client(timeout=10.0) as client:
        for endpoint in endpoints:
            signature = hmac_sha256(endpoint.secret, body)
            try:
                client.post(
                    endpoint.url,
                    content=body,
                    headers={
                        "content-type": "application/json",
                        "x-webhook-signature": signature,
                    },
                )
            except Exception as error:  # noqa: BLE001
                print(
                    json.dumps(
                        {
                            "endpoint": endpoint.url,
                            "status": "failed",
                            "failureReason": str(error),
                        }
                    )
                )
