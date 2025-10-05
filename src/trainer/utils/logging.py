"""Logging configuration utilities."""

import logging

from trainer.utils.config import settings

logger = logging.getLogger(__name__)


def setup_logging() -> None:
    """Configure logging for the application."""
    log_level = getattr(logging, settings.log_level.upper())

    # Configure logging format
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Set third-party library log levels to WARNING to reduce noise
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("google").setLevel(logging.WARNING)
    logging.getLogger("google_genai").setLevel(logging.ERROR)  # Suppress function_call warnings
    logging.getLogger("google_adk").setLevel(logging.ERROR)  # Suppress ADK warnings

    logger.info(f"Logging configured at {logging.getLevelName(log_level)} level")
