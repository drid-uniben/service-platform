from sqlalchemy.orm import Session

from app.models import Account, ApiKey


def create_account(db: Session, name: str) -> Account:
    account = Account(name=name)
    db.add(account)
    db.flush()
    return account


def create_api_key_record(db: Session, account_id: str, key_hash: str) -> ApiKey:
    api_key = ApiKey(key_hash=key_hash, account_id=account_id)
    db.add(api_key)
    return api_key


def get_api_key_by_hash(db: Session, key_hash: str) -> ApiKey | None:
    return db.query(ApiKey).filter(ApiKey.key_hash == key_hash).first()
