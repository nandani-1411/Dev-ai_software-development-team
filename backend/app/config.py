import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = "DevAI"
    VERSION: str = "0.1.0"
    PORT: int = int(os.getenv("PORT", "8000"))
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    MISTRAL_API_KEY: str = os.getenv("MISTRAL_API_KEY", "")


settings = Settings()
