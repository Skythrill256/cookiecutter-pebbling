import os
import sys
from pathlib import Path
from huggingface_hub import HfApi, create_repo, upload_folder
import tomli


def main():
    hf_token = os.environ.get("HF_TOKEN")
    if not hf_token:
        print("HF_TOKEN not set")
        sys.exit(1)

    api = HfApi(token=hf_token)
    try:
        username = api.whoami()["name"]
        print(f"Authenticated as {username}")
    except Exception as e:
        print(f"Authentication failed: {e}")
        sys.exit(1)

    # Get project name from pyproject.toml
    project_dir = Path.cwd().parent
    pyproject_file = project_dir / "pyproject.toml"
    if not pyproject_file.exists():
        print("pyproject.toml not found")
        sys.exit(1)

    try:
        with open(pyproject_file, "rb") as f:
            pyproject = tomli.load(f)
        project_name = pyproject.get("project", {}).get("name")
        if not project_name:
            print("Project name not found in pyproject.toml")
            sys.exit(1)
    except Exception as e:
        print(f"Could not read pyproject.toml: {e}")
        sys.exit(1)

    repo_id = f"{username}/{project_name}"
    print(f"\n🚀 Deploying project '{project_name}' -> {repo_id}")

    try:
        # Create HF Space (docker)
        create_repo(
            repo_id=repo_id,
            repo_type="space",
            space_sdk="docker",
            token=hf_token,
            exist_ok=True,
            private=False,
        )

        # Generate requirements.txt if pyproject.toml exists and requirements.txt missing
        generate_requirements(project_dir)

        # Upload project folder (includes Dockerfile, README.md, pyproject.toml, src/, etc.)
        upload_folder(
            folder_path=str(project_dir),
            repo_id=repo_id,
            repo_type="space",
            token=hf_token,
            commit_message=f"Deploy {project_name} with Docker setup",
            ignore_patterns=[".git", "__pycache__", "*.pyc", ".DS_Store"],
        )

        url = f"https://huggingface.co/spaces/{repo_id}"
        print(f"Deployed: {url}")

    except Exception as e:
        print(f"❌ Failed {project_name}: {e}")


def generate_requirements(project_dir: Path):
    """Generate requirements.txt from pyproject.toml if not exists"""
    req_file = project_dir / "requirements.txt"
    pyproject_file = project_dir / "pyproject.toml"

    if req_file.exists():
        return  # already exists

    if not pyproject_file.exists():
        return  # nothing to generate

    try:
        with open(pyproject_file, "rb") as f:
            pyproject = tomli.load(f)

        deps = pyproject.get("project", {}).get("dependencies", [])
        if deps:
            # make sure to exclude extras or invalid lines if any
            cleaned = [str(dep) for dep in deps]
            req_file.write_text("\n".join(cleaned))
            print("Generated requirements.txt from pyproject.toml")
    except Exception as e:
        print(f"Could not generate requirements.txt: {e}")


if __name__ == "__main__":
    main()
