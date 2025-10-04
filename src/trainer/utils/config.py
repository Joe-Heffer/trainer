"""Configuration management."""

import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv


def load_config() -> dict[str, Any]:
    """Load configuration from environment variables.

    Returns:
        Configuration dictionary
    """
    # Load from .env file if it exists
    env_file = Path(__file__).parent.parent.parent.parent / ".env"
    if env_file.exists():
        load_dotenv(env_file)

    return {
        "gemini_api_key": os.getenv("GEMINI_API_KEY"),
        "strava_mcp_url": os.getenv("STRAVA_MCP_URL", "http://localhost:3000"),
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
    }
