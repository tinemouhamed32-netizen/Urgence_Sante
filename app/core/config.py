import os
from typing import Final

PROJECT_NAME: Final[str] = "Urgence Santé"
API_VERSION: Final[str] = "0.1.0"
APP_ENV: Final[str] = os.getenv("APP_ENV", "development")
APP_DEBUG: Final[bool] = os.getenv("APP_DEBUG", "false").lower() == "true"
DEFAULT_COUNTRY: Final[str] = os.getenv("DEFAULT_COUNTRY", "SN")
MAX_UPLOAD_SIZE: Final[int] = 5 * 1024 * 1024
ALLOWED_IMAGE_TYPES: Final[set[str]] = {"image/jpeg", "image/png", "image/webp"}
SUPPORTED_LANGUAGES: Final[list[str]] = ["fr", "fr-SN", "en", "wo"]
SECRET_KEYS: Final[dict[str, str]] = {
    "APP_SECRET": os.getenv("APP_SECRET", "demo-secret-change-me"),
    "LLM_API_KEY": os.getenv("LLM_API_KEY", "demo-llm-key"),
}
