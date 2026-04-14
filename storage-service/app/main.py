from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.router import api_router
from app.core.errors import generic_exception_handler, http_exception_handler, validation_exception_handler
from app.core.request_context import request_context_middleware

app = FastAPI(title="Storage Service")
app.middleware("http")(request_context_middleware)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)
app.include_router(api_router)
