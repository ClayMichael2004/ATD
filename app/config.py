import os
from functools import lru_cache
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file if present
load_dotenv(BASE_DIR / ".env")


class Settings:
    """Application settings loaded from environment variables with sensible defaults."""

    def __init__(self) -> None:
        self.APP_NAME: str = os.getenv("APP_NAME", "AI Text Detection Engine")
        self.APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
        self.APP_ENV: str = os.getenv("APP_ENV", "development")
        self.DEBUG: bool = os.getenv("DEBUG", "true").lower() in ("true", "1", "yes")

        self.HOST: str = os.getenv("HOST", "0.0.0.0")
        self.PORT: int = int(os.getenv("PORT", "8000"))

        # Model and Tokenizer settings
        self.MODEL_PATH: str = os.getenv("MODEL_PATH", str(BASE_DIR / "saved_ai_detector"))
        self.MAX_SEQUENCE_LENGTH: int = int(os.getenv("MAX_SEQUENCE_LENGTH", "512"))
        self.DEVICE: str = os.getenv("DEVICE", "auto")

        # CORS settings
        self._cors_raw: str = os.getenv("CORS_ORIGINS", "*")

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
