FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install runtime dependencies only (no dev deps)
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir "pebble[slim]"
{% if cookiecutter.agent_framework == "agno" %}
RUN pip install --no-cache-dir agno
{% elif cookiecutter.agent_framework == "crew" %}
RUN pip install --no-cache-dir crewai
{% elif cookiecutter.agent_framework == "langchain" %}
RUN pip install --no-cache-dir langchain
{% endif %}

# Copy project files
COPY README.md ./
COPY src ./{{cookiecutter.name}}

# Default to running the module; adjust as needed
CMD ["python", "-m", "{{cookiecutter.name}}"]

