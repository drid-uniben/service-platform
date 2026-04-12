from sqlalchemy.orm import Session

from app.models import Account, ApiKey
from app.security import generate_api_key, sha256


def create_api_key(db: Session, account_name: str) -> dict[str, str]:
    account = Account(name=account_name)
    db.add(account)
    db.flush()

    plaintext_key = generate_api_key()
    key_hash = sha256(plaintext_key)

    db.add(ApiKey(key_hash=key_hash, account_id=account.id))
    db.commit()

    return {"accountId": account.id, "apiKey": plaintext_key}


def validate_api_key(db: Session, plaintext_api_key: str) -> ApiKey | None:
    key_hash = sha256(plaintext_api_key)
    return db.query(ApiKey).filter(ApiKey.key_hash == key_hash).first()
