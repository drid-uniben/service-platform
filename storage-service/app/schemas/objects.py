from datetime import datetime

from pydantic import BaseModel, HttpUrl, field_validator


class StoreObjectRequest(BaseModel):
    objectKey: str
    sourceUrl: HttpUrl
    contentType: str | None = None
    sizeBytes: int | None = None

    @field_validator("objectKey")
    @classmethod
    def validate_object_key(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("objectKey must be a string.")
        return value

    @field_validator("contentType")
    @classmethod
    def clean_content_type(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        return value or None

    @field_validator("sizeBytes")
    @classmethod
    def validate_size(cls, value: int | None) -> int | None:
        if value is not None and value < 1:
            raise ValueError("sizeBytes must be an integer greater than or equal to 1.")
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
    providerUsed: str | None
    storedUrl: str | None
    createdAt: datetime
