import json
import os
from typing import List

from pebbling.common.protocol.types import AgentCapabilities, AgentSkill
from pebbling.penguin.pebblify import pebblify
from pebbling.common.models import DeploymentConfig


def _load_config() -> dict:
    # Prefer stdlib tomllib (Py 3.11+) with fallback to tomli for Py 3.10
    try:
        import tomllib  # type: ignore[attr-defined]
    except Exception:  # pragma: no cover
        import tomli as tomllib  # type: ignore[no-redef]

    project_root = os.path.dirname(os.path.dirname(__file__))
    cfg_path = os.path.join(project_root, ".pebble", "agent_config.toml")
    with open(cfg_path, "rb") as f:
        return tomllib.load(f)


simple_config = _load_config()


@pebblify(
    author=simple_config["author"],
    name=simple_config.get("name"),
    description=simple_config.get("description"),
    version=simple_config.get("version", "1.0.0"),
    recreate_keys=simple_config.get("recreate_keys", True),
    skills=[AgentSkill(**skill) for skill in simple_config.get("skills", [])],
    capabilities=AgentCapabilities(**simple_config["capabilities"]),
    agent_trust=simple_config.get("agent_trust"),
    kind=simple_config.get("kind", "agent"),
    debug_mode=simple_config.get("debug_mode", False),
    debug_level=simple_config.get("debug_level", 1),
    monitoring=simple_config.get("monitoring", False),
    telemetry=simple_config.get("telemetry", True),
    num_history_sessions=simple_config.get("num_history_sessions", 10),
    documentation_url=simple_config.get("documentation_url"),
    extra_metadata=simple_config.get("extra_metadata", {}),
    deployment_config=DeploymentConfig(**simple_config["deployment"]),
)
def simple_agent(messages: List[str]) -> str:
    """Regular function example - returns single result."""
    {% if cookiecutter.agent_framework == "agno" %}
    from agno.agent import Agent
    from agno.models.openai import OpenAIChat

    agent = Agent(
        instructions="Provide a simple response to the user's message",
        model=OpenAIChat(id="gpt-4o"),
    )
    result = agent.run(messages=messages)
    try:
        return result.to_dict().get("content", str(result))
    except Exception:
        return str(result)
    {% elif cookiecutter.agent_framework == "crew" %}
    from crew import Agent  # per user instruction

    agent = Agent(
        instructions="Provide a simple response to the user's message",
    )
    result = agent.run(messages=messages)
    return getattr(result, "content", str(result))
    {% elif cookiecutter.agent_framework == "langchain" %}
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model="gpt-4o")
    prompt = messages[-1] if messages else "Hello"
    resp = llm.invoke(prompt)
    return getattr(resp, "content", str(resp))
    {% else %}
    return messages[-1] if messages else "Hello from {{ cookiecutter.name }}!"
    {% endif %}
