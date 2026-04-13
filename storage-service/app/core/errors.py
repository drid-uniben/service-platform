import json
from datetime import UTC, datetime

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def http_exception_handler(request: Request, exc: HTTPException):
    payload = exc.detail if exc.detail is not None else "Unhandled HTTP error"
    status_code = exc.status_code

    print(
        json.dumps(
            {
                "requestId": getattr(request.state, "request_id", "unknown"),
                "status": status_code,
                "path": request.url.path,
                "method": request.method,
                "error": payload,
            }
        )
    )

    return JSONResponse(
        status_code=status_code,
        content={
            "statusCode": status_code,
            "path": request.url.path,
            "requestId": getattr(request.state, "request_id", None),
            "error": payload,
            "timestamp": datetime.now(UTC).isoformat(),
        },
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return await http_exception_handler(
        request,
        HTTPException(
            status_code=400,
            detail={"message": "Validation failed.", "details": exc.errors()},
        ),
    )
