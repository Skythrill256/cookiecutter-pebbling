import json
import os
from typing import List

from pebbling.common.models import DeploymentConfig, SchedulerConfig, StorageConfig
from pebbling.common.protocol.types import AgentCapabilities, AgentSkill
from pebbling.penguin.pebblify import pebblify


def load_config(config_path: str):
    """Load configuration from JSON with defaults."""
    # Get the project root directory (parent of src)
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(current_dir, config_path)
    
    with open(full_path, 'r') as f:
        config = json.load(f)
        print(f"Loaded config from {full_path}")
        return config

simple_config = load_config(".pebble/agent_config.json")


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
    storage_config=StorageConfig(**simple_config["storage"]),
    scheduler_config=SchedulerConfig(**simple_config["scheduler"]),
)
def simple_agent(messages: List[str]) -> str:
    """Regular function example - returns single result."""
    
    from agno.agent import Agent
    from agno.models.openai import OpenAIChat
    
    agent = Agent(
        instructions="Provide a simple response to the user's message",
        model=OpenAIChat(id="gpt-4o")
    )
    
    result = agent.run(input=messages)
    return result.to_dict()['content']
