from pydantic import BaseModel, field_validator

from app.schemas.base import CamelModel


class CreateApiKeyRequest(CamelModel):
    account_name: str

    @field_validator("account_name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 2:
            raise ValueError("account_name must be a string with at least 2 characters.")
        return value


class CreateApiKeyResponse(BaseModel):
    accountId: str
    apiKey: str
