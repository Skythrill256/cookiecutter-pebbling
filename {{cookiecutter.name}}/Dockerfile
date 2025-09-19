FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency files
COPY pyproject.toml ./

# Sync dependencies into system, then uninstall uv
RUN uv sync --group dev

# Copy project files
COPY README.md ./
COPY src ./{{cookiecutter.name}}

COPY .pebble/ ./.pebble/

ENV PYTHONPATH=/app/src

# Run the app
CMD ["uv", "run", "python", "-m", "main"]

