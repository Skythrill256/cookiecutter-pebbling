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

