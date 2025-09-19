
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml ./
RUN uv pip install --system --no-cache .
RUN pip uninstall -y uv

COPY README.md ./
COPY {{cookiecutter.name}} ./{{cookiecutter.name}}

CMD ["python", "-m", "{{cookiecutter.name}}"]
