import os
from functools import lru_cache
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file if present
load_dotenv(BASE_DIR / ".env")


class Settings:
    """Application settings loaded from environment variables with sensible defaults."""

    APP_NAME: str = os.getenv("APP_NAME", "AI Text Detection Engine")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() in ("true", "1", "yes")

    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    # Model and Tokenizer settings
    MODEL_PATH: str = os.getenv("MODEL_PATH", str(BASE_DIR / "saved_ai_detector"))
    MAX_SEQUENCE_LENGTH: int = int(os.getenv("MAX_SEQUENCE_LENGTH", "512"))
    DEVICE: str = os.getenv("DEVICE", "auto")

    # CORS settings
    _cors_raw: str = os.getenv("CORS_ORIGINS", "*")

    @property
    def cors_origins(self) -> list[str]:
        if not self._cors_raw or self._cors_raw.strip() == "*":
            return ["*"]
        return [origin.strip() for origin in self._cors_raw.split(",") if origin.strip()]

    @property
    def resolved_model_path(self) -> Path:
        path = Path(self.MODEL_PATH)
        if not path.is_absolute():
            path = BASE_DIR / path
        return path.resolve()


@lru_cache()
def get_settings() -> Settings:
    return Settings()
