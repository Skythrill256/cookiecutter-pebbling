FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app


RUN pip install --no-cache-dir uv

COPY pyproject.toml ./


RUN uv sync --group dev


COPY README.md ./
COPY src ./src/

COPY .pebble/ ./.pebble/

ENV PYTHONPATH=/app/src


CMD ["uv", "run", "python", "-m", "main.py"]


