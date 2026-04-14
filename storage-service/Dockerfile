FROM python:3.12-slim AS runtime

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.8.15 /uv /usr/local/bin/uv

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV STORAGE_ROOT=/data/drid/storage
ENV UV_LINK_MODE=copy
ENV PYTHONPATH=/app

COPY pyproject.toml uv.lock ./

RUN uv sync --no-dev --frozen

COPY app ./app
COPY alembic ./alembic
COPY alembic.ini ./alembic.ini

VOLUME ["/data/drid/storage"]
EXPOSE 3000

CMD ["sh", "-c", "uv run alembic upgrade head && uv run uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-3000}"]