from pydantic import BaseModel, field_validator


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
