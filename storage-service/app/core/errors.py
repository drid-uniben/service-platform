import logging
from datetime import UTC, datetime

from fastapi import HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


logger = logging.getLogger(__name__)


def _error_payload(detail: object, fallback_message: str) -> object:
    if detail is None:
        return {"message": fallback_message}

    if isinstance(detail, dict):
        return detail

    if isinstance(detail, list):
        return {"message": fallback_message, "details": detail}

    return {"message": str(detail)}


async def http_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, StarletteHTTPException):
        status_code = exc.status_code
        payload = _error_payload(exc.detail, "Unhandled HTTP error")
    else:
        status_code = 500
        payload = {"message": "Unhandled HTTP error"}

    logger.info(
        "http_exception",
        extra={
            "requestId": getattr(request.state, "request_id", "unknown"),
            "status": status_code,
            "path": request.url.path,
            "method": request.method,
            "error": payload,
        },
    )

    return JSONResponse(
        status_code=status_code,
        content={
            "statusCode": status_code,
            "path": request.url.path,
            "requestId": getattr(request.state, "request_id", None),
            "error": jsonable_encoder(payload),
            "timestamp": datetime.now(UTC).isoformat(),
        },
    )


async def validation_exception_handler(request: Request, exc: Exception):
    validation_error = exc if isinstance(exc, RequestValidationError) else RequestValidationError([])
    return await http_exception_handler(
        request,
        HTTPException(
            status_code=400,
            detail={"message": "Validation failed.", "details": jsonable_encoder(validation_error.errors())},
        ),
    )


async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception(
        "unhandled_exception",
        extra={
            "requestId": getattr(request.state, "request_id", "unknown"),
            "path": request.url.path,
            "method": request.method,
        },
    )

    return JSONResponse(
        status_code=500,
        content={
            "statusCode": 500,
            "path": request.url.path,
            "requestId": getattr(request.state, "request_id", None),
            "error": {"message": "Internal server error"},
            "timestamp": datetime.now(UTC).isoformat(),
        },
    )
