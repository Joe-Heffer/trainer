"""Main entry point for the trainer CLI."""

import asyncio
import logging
import sys

from trainer.agents.trainer_agent import TrainerAgent
from trainer.utils.arguments import parse_arguments
from trainer.utils.config import get_settings
from trainer.utils.logging import setup_logging

logger = logging.getLogger(__name__)


async def async_main() -> int:
    """Async main function that runs the trainer agent."""
    # Load .env file for CLI usage (not done at import time for test speed)
    get_settings(load_dotenv_file=True)

    setup_logging()
    logger.info("Starting trAIner CLI")

    print("🏃 trAIner - Your AI Personal Trainer")
    print("=" * 40)

    try:
        logger.debug("Creating agent")
        agent = TrainerAgent()
        await agent.run_interactive()

    except Exception as e:
        logger.error(f"Error occurred: {e}", exc_info=True)
        print(f"\n❌ Error: {e}", file=sys.stderr)
        return 1
    finally:
        # Cleanup MCP session
        try:
            from trainer.tools import close_mcp_session

            await close_mcp_session()
        except Exception:
            pass

    logger.info("trAIner CLI shutting down")
    return 0


def main() -> int:
    """Entry point for the trainer CLI."""
    parse_arguments()
    return asyncio.run(async_main())


if __name__ == "__main__":
    sys.exit(main())
