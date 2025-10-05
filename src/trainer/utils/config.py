"""Configuration management."""

import logging
import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


@dataclass
class Settings:
    """Application settings loaded from environment variables."""

    gemini_api_key: str | None = None
    strava_mcp_path: str | None = None
    log_level: str = "INFO"


# Global settings instance - created lazily
_settings: Settings | None = None


def get_settings(load_dotenv_file: bool = False) -> Settings:
    """Get or create the global settings instance.

    Args:
        load_dotenv_file: Whether to load from .env file (slow on WSL, disabled by default)

    Returns:
        Application settings
    """
    global _settings

    # If load_dotenv_file is requested, reset settings to reload from .env
    if load_dotenv_file:
        _settings = None

    if _settings is None:
        # Only load .env file if explicitly requested (e.g., in CLI main)
        if load_dotenv_file:
            env_file = Path(__file__).parent.parent.parent.parent / ".env"
            if env_file.exists():
                logger.info(f"Loading configuration from {env_file}")
                load_dotenv(env_file)
            else:
                logger.debug(f".env file not found at {env_file}, using environment variables only")

        # Load from environment variables
        # Use GOOGLE_API_KEY (standard Google SDK env var) or fall back to GEMINI_API_KEY
        _settings = Settings(
            gemini_api_key=os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY"),
            strava_mcp_path=os.getenv("STRAVA_MCP_PATH"),
            log_level=os.getenv("LOG_LEVEL", "WARNING"),
        )

    return _settings


# Create settings instance - will use env vars (pytest sets these before import)
settings = get_settings()
