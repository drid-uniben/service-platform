import json
import re
from urllib.parse import parse_qsl, urlencode

from fastapi import Request
from fastapi.routing import APIRoute
from starlette.datastructures import FormData

_CAMEL_BOUNDARY = re.compile(r"(?<!^)(?=[A-Z])")


def to_snake_case(value: str) -> str:
    return _CAMEL_BOUNDARY.sub("_", value).lower()


def to_camel_case(value: str) -> str:
    parts = value.split("_")
    return parts[0] + "".join(part.capitalize() for part in parts[1:])


def _key_variants(key: str) -> list[str]:
    snake_key = to_snake_case(key)
    camel_key = to_camel_case(snake_key)
    variants: list[str] = []
    for candidate in (key, snake_key, camel_key):
        if candidate not in variants:
            variants.append(candidate)
    return variants


def normalize_json_payload(value):
    if isinstance(value, dict):
        return {to_snake_case(key): normalize_json_payload(item) for key, item in value.items()}
    if isinstance(value, list):
        return [normalize_json_payload(item) for item in value]
    return value


def normalize_query_string(raw_query: bytes) -> bytes:
    if not raw_query:
        return raw_query

    pairs = parse_qsl(raw_query.decode("utf-8"), keep_blank_values=True)
    normalized_pairs: list[tuple[str, str]] = []
    for key, value in pairs:
        for candidate in _key_variants(key):
            normalized_pairs.append((candidate, value))
    return urlencode(normalized_pairs, doseq=True).encode("utf-8")


async def normalize_request_to_snake_case(request: Request) -> None:
    request.scope["query_string"] = normalize_query_string(request.scope.get("query_string", b""))

    content_type = request.headers.get("content-type", "").split(";", 1)[0].strip().lower()

    if content_type == "application/json":
        body = await request.body()
        if body:
            try:
                normalized_json = normalize_json_payload(json.loads(body))
                normalized_body = json.dumps(normalized_json).encode("utf-8")
                request._body = normalized_body
                request._json = normalized_json
            except json.JSONDecodeError:
                pass

    if content_type in {"application/x-www-form-urlencoded", "multipart/form-data"}:
        form = await request.form()
        normalized_items = []
        for key, value in form.multi_items():
            for candidate in _key_variants(key):
                normalized_items.append((candidate, value))
        request._form = FormData(normalized_items)


class SnakeCaseRoute(APIRoute):
    def get_route_handler(self):
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request):
            await normalize_request_to_snake_case(request)
            return await original_route_handler(request)

        return custom_route_handler