FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency files
COPY pyproject.toml ./

# Sync dependencies into system, then uninstall uv
RUN uv pip install --system --no-cache . \
    && pip uninstall -y uv

# Copy project files
COPY README.md ./
COPY src ./{{cookiecutter.name}}

# Run the app
CMD ["python", "-m", "{{cookiecutter.name}}"]
