from sqlalchemy.orm import Session

from app.models import AttemptStatus, FileVisibility, ObjectStatus, ProviderAttempt, StorageObject


def create_storage_object(
    db: Session,
    account_id: str,
    object_key: str,
    source_url: str,
    content_type: str | None,
    size_bytes: int | None,
    visibility: FileVisibility = FileVisibility.private,
) -> StorageObject:
    storage_object = StorageObject(
        account_id=account_id,
        object_key=object_key,
        source_url=source_url,
        content_type=content_type,
        size_bytes=size_bytes,
        status=ObjectStatus.queued,
        visibility=visibility,
    )
    db.add(storage_object)
    return storage_object


def get_storage_object_for_account(db: Session, account_id: str, object_id: str) -> StorageObject | None:
    return (
        db.query(StorageObject)
        .filter(StorageObject.id == object_id, StorageObject.account_id == account_id)
        .first()
    )


def get_storage_object_by_id(db: Session, storage_object_id: str) -> StorageObject | None:
    return db.query(StorageObject).filter(StorageObject.id == storage_object_id).first()


def get_public_storage_object_by_account_and_key(
    db: Session,
    account_id: str,
    object_key: str,
) -> StorageObject | None:
    return (
        db.query(StorageObject)
        .filter(
            StorageObject.account_id == account_id,
            StorageObject.object_key == object_key,
            StorageObject.visibility == FileVisibility.public,
        )
        .first()
    )


def add_provider_attempt(
    db: Session,
    storage_object_id: str,
    provider: str,
    status: AttemptStatus,
    error_message: str | None = None,
) -> ProviderAttempt:
    attempt = ProviderAttempt(
        storage_object_id=storage_object_id,
        provider=provider,
        status=status,
        error_message=error_message,
    )
    db.add(attempt)
    return attempt
