from datetime import datetime

from pydantic import BaseModel, HttpUrl, field_validator


class CreateApiKeyRequest(BaseModel):
    accountName: str

    @field_validator("accountName")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 2:
            raise ValueError("accountName must be a string with at least 2 characters.")
        return value


class CreateApiKeyResponse(BaseModel):
    accountId: str
    apiKey: str


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


class RegisterWebhookRequest(BaseModel):
    url: HttpUrl
    secret: str

    @field_validator("secret")
    @classmethod
    def validate_secret(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("secret must be a string.")
        return value


class WebhookEndpointResponse(BaseModel):
    id: str
    accountId: str
    url: str
    secret: str
    createdAt: datetime


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
