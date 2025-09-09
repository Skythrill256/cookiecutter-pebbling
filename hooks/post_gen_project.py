import sys


def main() -> None:
    project_name = "{{ cookiecutter.name }}"
    agent = "{{ cookiecutter.agent_framework }}"

    lines = [
        "\n🎉 Project created successfully!\n",
        "🐧 Welcome to Pebbling — powered by the Pebble CLI.",
        "Next steps:",
        f"  1️⃣  cd '{project_name}'",
        "  2️⃣  Set it up using uv: 📦",
        "      uv sync",
        "  3️⃣  Run your agent locally: 💻",
        f"      PYTHONPATH=src python3 -m {project_name}",
        "      or",
        "      python3 src/<filename.py>",
        "  4️⃣  Deploy your agent: 🚀",
        "      pebble launch"
    ]
    if agent and agent != "none":
        lines.append(f"\n🤖 Selected agent framework: {agent}")

    lines.append("Need help? See README.md for details. ✨")
    print("\n".join(lines))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"⚠️  Post-generation message failed: {exc}", file=sys.stderr)
