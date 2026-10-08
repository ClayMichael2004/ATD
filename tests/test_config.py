import os
from pathlib import Path
from unittest.mock import patch

from app.config import Settings


def test_default_settings():
    settings = Settings()
    assert settings.APP_NAME is not None
    assert settings.PORT == 8000
    assert settings.MAX_SEQUENCE_LENGTH == 512
    assert "*" in settings.cors_origins


def test_cors_origins_parsing():
    with patch.dict(os.environ, {"CORS_ORIGINS": "http://localhost:3000, https://myapp.com"}):
        settings = Settings()
        assert settings.cors_origins == ["http://localhost:3000", "https://myapp.com"]


def test_cors_origins_wildcard():
    with patch.dict(os.environ, {"CORS_ORIGINS": "*"}):
        settings = Settings()
        assert settings.cors_origins == ["*"]


def test_resolved_model_path():
    settings = Settings()
    resolved = settings.resolved_model_path
    assert isinstance(resolved, Path)
    assert resolved.is_absolute()
