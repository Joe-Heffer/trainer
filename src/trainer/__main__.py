"""Main entry point for the trainer CLI."""

import asyncio
import logging
import sys

from trainer.agents.trainer_agent import TrainerAgent
from trainer.utils.arguments import parse_arguments
from trainer.utils.logging import setup_logging

logger = logging.getLogger(__name__)


async def async_main() -> int:
    """Async main function that runs the trainer agent."""
    setup_logging()
    logger.info("Starting trAIner CLI")

    print("🏃 trAIner - Your AI Personal Trainer")
    print("=" * 40)

    agent = TrainerAgent()

    try:
        logger.debug("Initializing agent")
        await agent.initialize()
        await agent.run_interactive()

    except Exception as e:
        logger.error(f"Error occurred: {e}", exc_info=True)
        print(f"\n❌ Error: {e}", file=sys.stderr)
        return 1

    logger.info("trAIner CLI shutting down")
    return 0


def main() -> int:
    """Entry point for the trainer CLI."""
    parse_arguments()
    return asyncio.run(async_main())


if __name__ == "__main__":
    sys.exit(main())
