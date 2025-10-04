"""Configuration management."""

import logging
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


def load_config() -> dict[str, Any]:
    """Load configuration from environment variables.

    Returns:
        Configuration dictionary
    """
    # Load from .env file if it exists
    env_file = Path(__file__).parent.parent.parent.parent / ".env"
    if env_file.exists():
        logger.info(f"Loading configuration from {env_file}")
        load_dotenv(env_file)
    else:
        logger.warning(f".env file not found at {env_file}, using environment variables only")

    config = {
        "gemini_api_key": os.getenv("GEMINI_API_KEY"),
        "strava_mcp_url": os.getenv("STRAVA_MCP_URL", "http://localhost:3000"),
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
    }

    # Log config loaded (but mask sensitive data)
    safe_config = {k: ("***" if "key" in k.lower() else v) for k, v in config.items()}
    logger.debug(f"Configuration loaded: {safe_config}")

    return config
