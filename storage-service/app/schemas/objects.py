from datetime import datetime

from pydantic import BaseModel, HttpUrl, field_validator

from app.models.enums import FileVisibility
from app.schemas.base import CamelModel


class StoreObjectRequest(CamelModel):
    object_key: str
    source_url: HttpUrl
    content_type: str | None = None
    size_bytes: int | None = None
    visibility: FileVisibility = FileVisibility.private

    @field_validator("object_key")
    @classmethod
    def validate_object_key(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("object_key must be a string.")
        return value

    @field_validator("content_type")
    @classmethod
    def clean_content_type(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        return value or None

    @field_validator("size_bytes")
    @classmethod
    def validate_size(cls, value: int | None) -> int | None:
        if value is not None and value < 1:
            raise ValueError("size_bytes must be an integer greater than or equal to 1.")
        return value


class QueueStorageResponse(BaseModel):
    id: str
    status: str


class StorageObjectResponse(BaseModel):
    id: str
    accountId: str
    objectKey: str
    sourceUrl: str
    contentType: str | None
    sizeBytes: int | None
    status: str
    visibility: FileVisibility
    providerUsed: str | None
    storedUrl: str | None
    createdAt: datetime
