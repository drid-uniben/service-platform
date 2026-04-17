from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, Request, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.core.case_normalizer import SnakeCaseRoute
from app.db import get_db
from app.dependencies.auth import require_api_key
from app.models.enums import FileVisibility
from app.schemas.mappers import to_storage_object_response
from app.schemas.objects import QueueStorageResponse, StorageObjectResponse, StoreObjectRequest
from app.services.storage_service import (
    get_public_file_path,
    get_status,
    process_storage_object,
    queue_storage,
    store_uploaded_object,
    validate_object_key_path,
)

router = APIRouter(prefix="/objects", tags=["objects"], route_class=SnakeCaseRoute)


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
    validate_object_key_path(settings, account_id, payload.object_key)

    storage_object = queue_storage(
        db,
        account_id,
        payload.object_key,
        str(payload.source_url),
        payload.content_type,
        payload.size_bytes,
        payload.visibility,
    )

    background_tasks.add_task(
        process_storage_object,
        storage_object.id,
        getattr(request.state, "request_id", None),
        settings,
    )

    return {"id": storage_object.id, "status": "queued"}


@router.post("/upload", response_model=StorageObjectResponse, status_code=201)
def upload_storage_route(
    request: Request,
    objectKey: str = Form(...),  # Keep camelCase here: multipart OpenAPI uses route Form param names in this FastAPI version.
    file: UploadFile = File(...),
    visibility: FileVisibility = Form(default=FileVisibility.private),
    auth: tuple[str, str] = Depends(require_api_key),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    account_id, _ = auth
    object_key = objectKey
    validate_object_key_path(settings, account_id, object_key)

    storage_object = store_uploaded_object(
        db,
        account_id,
        object_key,
        file,
        settings,
        getattr(request.state, "request_id", None),
        visibility,
    )

    return to_storage_object_response(storage_object)


@router.get("/public/{account_id}/{object_key:path}", response_class=FileResponse)
def get_public_file_route(
    account_id: str,
    object_key: str,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
):
    file_path, storage_object = get_public_file_path(db, settings, account_id, object_key)
    return FileResponse(path=file_path, media_type=storage_object.content_type or None)


@router.get("/{object_id}", response_model=StorageObjectResponse)
def get_storage_status_route(
    object_id: str,
    auth: tuple[str, str] = Depends(require_api_key),
    db: Session = Depends(get_db),
):
    account_id, _ = auth
    storage_object = get_status(db, account_id, object_id)
    return to_storage_object_response(storage_object)
