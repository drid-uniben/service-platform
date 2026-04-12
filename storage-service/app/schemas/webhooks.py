from datetime import datetime

from pydantic import BaseModel, HttpUrl, field_validator


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
