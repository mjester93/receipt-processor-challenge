FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:0.5.2 /uv /bin/uv

COPY . /app

WORKDIR /app

RUN uv sync --frozen --no-cache

EXPOSE 8000

CMD [".venv/bin/fastapi", "run", "api/main.py"]
