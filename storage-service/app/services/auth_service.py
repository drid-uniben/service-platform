from sqlalchemy.orm import Session

from app.models import ApiKey
from app.repositories.auth_repository import create_account, create_api_key_record, get_api_key_by_hash
from app.security import generate_api_key, sha256


def create_api_key(db: Session, account_name: str) -> dict[str, str]:
    account = create_account(db, account_name)

    plaintext_key = generate_api_key()
    key_hash = sha256(plaintext_key)

    create_api_key_record(db, account.id, key_hash)
    db.commit()

    return {"accountId": account.id, "apiKey": plaintext_key}


def validate_api_key(db: Session, plaintext_api_key: str) -> ApiKey | None:
    key_hash = sha256(plaintext_api_key)
    return get_api_key_by_hash(db, key_hash)
