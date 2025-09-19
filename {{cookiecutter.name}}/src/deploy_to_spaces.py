import os
import sys
import logging
from pathlib import Path
from huggingface_hub import HfApi, create_repo, upload_folder

REPO_TYPE = "space"
SPACE_SDK = "docker"
IGNORE_PATTERNS = [".git", "__pycache__", "*.pyc", ".DS_Store", ".venv"]
COMMIT_MESSAGE = "Deploy {project_name} with Docker setup"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

def main():
    hf_token = os.environ.get("HF_TOKEN")
    if not hf_token:
        logging.error("HF_TOKEN not set")
        sys.exit(1)

    api = HfApi(token=hf_token)
    try:
        username = api.whoami()["name"]
        logging.info(f"Authenticated as {username}")
    except Exception as e:
        logging.error(f"Authentication failed: {e}")
        sys.exit(1)

    project_dir = Path.cwd()
    project_name = project_dir.name

    repo_id = f"{username}/{project_name}"
    logging.info(f"Deploying project '{project_name}' -> {repo_id}")

    try:
        create_repo(
            repo_id=repo_id,
            repo_type=REPO_TYPE,
            space_sdk=SPACE_SDK,
            token=hf_token,
            exist_ok=True,
            private=False,
        )

        upload_folder(
            folder_path=str(project_dir),
            repo_id=repo_id,
            repo_type=REPO_TYPE,
            token=hf_token,
            commit_message=COMMIT_MESSAGE.format(project_name=project_name),
            ignore_patterns=IGNORE_PATTERNS,
        )

        url = f"https://huggingface.co/spaces/{repo_id}"
        logging.info(f"Deployed: {url}")

    except Exception as e:
        logging.error(f"Failed {project_name}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
