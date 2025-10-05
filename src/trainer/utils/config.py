"""Configuration management."""

import logging
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)

# Load .env file at module import
env_file = Path(__file__).parent.parent.parent.parent / ".env"
if env_file.exists():
    logger.info(f"Loading configuration from {env_file}")
    load_dotenv(env_file)
else:
    logger.warning(f".env file not found at {env_file}, using environment variables only")


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    gemini_api_key: str | None = None
    strava_mcp_path: str | None = None
    log_level: str = "INFO"

    class Config:
        """Pydantic settings config."""

        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
