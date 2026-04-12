import json
from pathlib import Path

import httpx
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.config import Settings
from app.db import SessionLocal
from app.models import AttemptStatus, ObjectStatus, StorageObject
from app.repositories.storage_repository import (
    add_provider_attempt,
    create_storage_object,
    get_storage_object_by_id,
    get_storage_object_for_account,
)
from app.storage_paths import InvalidObjectKeyError, resolve_storage_path
from app.services.webhook_service import emit_storage_event


def queue_storage(
    db: Session,
    account_id: str,
    object_key: str,
    source_url: str,
    content_type: str | None,
    size_bytes: int | None,
) -> StorageObject:
    storage_object = create_storage_object(db, account_id, object_key, source_url, content_type, size_bytes)
    db.commit()
    db.refresh(storage_object)
    return storage_object


def get_status(db: Session, account_id: str, object_id: str) -> StorageObject:
    storage_object = get_storage_object_for_account(db, account_id, object_id)
    if not storage_object:
        raise HTTPException(status_code=404, detail="Storage object not found.")
    return storage_object


def validate_object_key_path(settings: Settings, account_id: str, object_key: str) -> None:
    try:
        resolve_storage_path(settings.storage_root, account_id, object_key)
    except InvalidObjectKeyError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


def process_storage_object(storage_object_id: str, request_id: str | None, settings: Settings) -> None:
    db = SessionLocal()
    try:
        storage_object = get_storage_object_by_id(db, storage_object_id)
        if not storage_object:
            return

        try:
            with httpx.Client(timeout=30.0, follow_redirects=True) as client:
                response = client.get(storage_object.source_url)
                response.raise_for_status()
                data = response.content

            absolute_path, relative_path = resolve_storage_path(
                settings.storage_root,
                storage_object.account_id,
                storage_object.object_key,
            )
            Path(absolute_path).parent.mkdir(parents=True, exist_ok=True)
            Path(absolute_path).write_bytes(data)

            add_provider_attempt(db, storage_object.id, "vps-disk", AttemptStatus.stored)

            storage_object.status = ObjectStatus.stored
            storage_object.provider_used = "vps-disk"
            storage_object.stored_url = relative_path
            db.commit()

            print(
                json.dumps(
                    {
                        "requestId": request_id,
                        "provider": "vps-disk",
                        "status": "stored",
                        "storageObjectId": storage_object.id,
                    }
                )
            )

            emit_storage_event(
                db,
                storage_object.account_id,
                {
                    "objectId": storage_object.id,
                    "status": "stored",
                    "objectPath": relative_path,
                },
            )
        except Exception as error:  # noqa: BLE001
            failure_reason = str(error)

            add_provider_attempt(
                db,
                storage_object.id,
                "vps-disk",
                AttemptStatus.failed,
                error_message=failure_reason,
            )

            storage_object.status = ObjectStatus.failed
            storage_object.provider_used = "vps-disk"
            db.commit()

            print(
                json.dumps(
                    {
                        "requestId": request_id,
                        "provider": "vps-disk",
                        "status": "failed",
                        "storageObjectId": storage_object.id,
                        "failureReason": failure_reason,
                    }
                )
            )

            emit_storage_event(
                db,
                storage_object.account_id,
                {
                    "objectId": storage_object.id,
                    "status": "failed",
                    "failureReason": failure_reason,
                },
            )
    finally:
        db.close()
