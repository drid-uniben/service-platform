import json
import time
import uuid

from fastapi import Request


async def request_context_middleware(request: Request, call_next):
    request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
    request.state.request_id = request_id

    start = time.time()
    response = await call_next(request)
    latency_ms = int((time.time() - start) * 1000)
    response.headers["x-request-id"] = request_id

    print(
        json.dumps(
            {
                "requestId": request_id,
                "method": request.method,
                "path": request.url.path,
                "status": response.status_code,
                "latencyMs": latency_ms,
            }
        )
    )

    return response
