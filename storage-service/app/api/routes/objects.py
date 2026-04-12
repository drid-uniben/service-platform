from fastapi import APIRouter, BackgroundTasks, Depends, Request
from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.db import get_db
from app.dependencies.auth import require_api_key
from app.schemas.mappers import to_storage_object_response
from app.schemas.objects import QueueStorageResponse, StorageObjectResponse, StoreObjectRequest
from app.services.storage_service import (
    get_status,
    process_storage_object,
    queue_storage,
    validate_object_key_path,
)

router = APIRouter(prefix="/objects", tags=["objects"])


@router.post("/store", response_model=QueueStorageResponse, status_code=202)
def queue_storage_route(
    payload: StoreObjectRequest,
    background_tasks: BackgroundTasks,
    request: Request,
    auth: tuple[str, str] = Depends(require_api_key),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    account_id, _ = auth
    validate_object_key_path(settings, account_id, payload.objectKey)

    storage_object = queue_storage(
        db,
        account_id,
        payload.objectKey,
        str(payload.sourceUrl),
        payload.contentType,
        payload.sizeBytes,
    )

    background_tasks.add_task(
        process_storage_object,
        storage_object.id,
        getattr(request.state, "request_id", None),
        settings,
    )

    return {"id": storage_object.id, "status": "queued"}


@router.get("/{object_id}", response_model=StorageObjectResponse)
def get_storage_status_route(
    object_id: str,
    auth: tuple[str, str] = Depends(require_api_key),
    db: Session = Depends(get_db),
):
    account_id, _ = auth
    storage_object = get_status(db, account_id, object_id)
    return to_storage_object_response(storage_object)
