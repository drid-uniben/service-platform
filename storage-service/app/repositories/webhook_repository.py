from sqlalchemy.orm import Session

from app.models import WebhookEndpoint


def create_webhook_endpoint(db: Session, account_id: str, url: str, secret: str) -> WebhookEndpoint:
    endpoint = WebhookEndpoint(account_id=account_id, url=url, secret=secret)
    db.add(endpoint)
    return endpoint


def get_webhook_endpoints_for_account(db: Session, account_id: str) -> list[WebhookEndpoint]:
    return db.query(WebhookEndpoint).filter(WebhookEndpoint.account_id == account_id).all()
