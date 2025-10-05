"""trAIner - An agentic AI personal trainer for fitness and health."""

from importlib.metadata import PackageNotFoundError, version

from .agents.trainer_agent import TrainerAgent

try:
    __version__ = version("trainer")
except PackageNotFoundError:
    __version__ = "0.0.0+unknown"


__all__ = ["TrainerAgent"]
