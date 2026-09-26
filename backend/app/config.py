import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

WORKSPACE_PATH = os.getenv("WORKSPACE_PATH", "D:/DevAI/workspaces")
workspace = Path(WORKSPACE_PATH)
if not workspace.exists():
    workspace.mkdir(parents=True, exist_ok=True)


class Settings:
    PROJECT_NAME: str = "DevAI"
    VERSION: str = "0.1.0"
    PORT: int = int(os.getenv("PORT", "8000"))
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    MISTRAL_API_KEY: str = os.getenv("MISTRAL_API_KEY", "")
    WORKSPACE_PATH: str = WORKSPACE_PATH


settings = Settings()
