---
title: {{ cookiecutter.name }}
emoji: 🤖
colorFrom: indigo
colorTo: pink
sdk: docker
sdk_version: "0.0.1"
app_port: 7860
pinned: false
---


# {{ cookiecutter.name }}

{{ cookiecutter.description }}

{% if cookiecutter.agent_framework != "none" %}
Selected agent framework: `{{ cookiecutter.agent_framework }}`
{% endif %}

## Development

- Runtime deps are in `pyproject.toml` under `[project.dependencies]`.
- Dev deps use uv dependency groups via `[dependency-groups]`.
  - Install dev deps with uv: `uv sync --group dev`

## Run

```
python -m {{ cookiecutter.name }}
```

