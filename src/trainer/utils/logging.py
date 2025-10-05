"""Logging configuration utilities."""

import logging

from trainer.utils.config import load_config

logger = logging.getLogger(__name__)


def setup_logging() -> None:
    """Configure logging for the application."""
    config = load_config()
    log_level = getattr(logging, config.get("log_level", "INFO").upper())

    # Configure logging format
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Set third-party library log levels to WARNING to reduce noise
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("google").setLevel(logging.WARNING)

    logger.info(f"Logging configured at {logging.getLevelName(log_level)} level")
