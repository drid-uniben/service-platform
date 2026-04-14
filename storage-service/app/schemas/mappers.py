from app.models import StorageObject, WebhookEndpoint


def to_storage_object_response(storage_object: StorageObject) -> dict:
    return {
        "id": storage_object.id,
        "accountId": storage_object.account_id,
        "objectKey": storage_object.object_key,
        "sourceUrl": storage_object.source_url,
        "contentType": storage_object.content_type,
        "sizeBytes": storage_object.size_bytes,
        "status": storage_object.status.value,
        "visibility": storage_object.visibility.value,
        "providerUsed": storage_object.provider_used,
        "storedUrl": storage_object.stored_url,
        "createdAt": storage_object.created_at,
    }


def to_webhook_endpoint_response(endpoint: WebhookEndpoint) -> dict:
    return {
        "id": endpoint.id,
        "accountId": endpoint.account_id,
        "url": endpoint.url,
        "secret": endpoint.secret,
        "createdAt": endpoint.created_at,
    }
