import os
import sys
from pathlib import Path
from huggingface_hub import HfApi, create_repo, upload_folder


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

    # Use current folder name as project name
    project_dir = Path.cwd()
    project_name = project_dir.name

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

        # Upload project folder (includes Dockerfile, README.md, src/, etc.)
        upload_folder(
            folder_path=str(project_dir),
            repo_id=repo_id,
            repo_type="space",
            token=hf_token,
            commit_message=f"Deploy {project_name} with Docker setup",
            ignore_patterns=[".git", "__pycache__", "*.pyc", ".DS_Store", ".venv"],
        )

        url = f"https://huggingface.co/spaces/{repo_id}"
        print(f"Deployed: {url}")

    except Exception as e:
        print(f"❌ Failed {project_name}: {e}")


if __name__ == "__main__":
    main()
