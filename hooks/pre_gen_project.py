import re
from cookiecutter.exceptions import FailedHookException


def fail(msg: str) -> None:
    raise FailedHookException("pre_gen_project validation failed: " + msg)


# Collected user inputs
NAME = "{{ cookiecutter.name }}"
PEBBLING_EMAIL = "{{ cookiecutter.pebbling_email }}".strip()
AGENT = "{{ cookiecutter.agent_framework }}"


# Strict validations
# 1) name: valid Python package identifier style: lowercase, starts with a letter, digits/underscores allowed
NAME_RE = re.compile(r"^[a-z][a-z0-9_]{2,}$")
if not NAME_RE.match(NAME):
    fail(
        "name must be a valid package name: start with a lowercase letter, "
        "contain only lowercase letters, digits, or underscores, and be at least 3 characters (e.g., 'pebble_project')."
    )

# 2) Optional email: if provided, check basic email format
if PEBBLING_EMAIL:
    EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    if not EMAIL_RE.match(PEBBLING_EMAIL):
        fail("pebbling_email is not a valid email address.")

# 3) Agent framework choice must be one of the allowed options
ALLOWED_AGENTS = {"none", "agno", "crew", "langchain"}
if AGENT not in ALLOWED_AGENTS:
    fail(f"agent_framework must be one of: {', '.join(sorted(ALLOWED_AGENTS))}.")

