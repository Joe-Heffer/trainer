"""Main entry point for the trainer CLI."""

import asyncio
import logging
import sys

from trainer.agents.trainer_agent import TrainerAgent
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
        print("\nAgent initialized. Type 'quit' or 'exit' to stop.\n")

        while True:
            try:
                user_input = input("You: ").strip()

                if user_input.lower() in ("quit", "exit", "q"):
                    logger.info("User requested exit")
                    print("\n👋 Thanks for training with trAIner!")
                    break

                if not user_input:
                    continue

                logger.debug(f"User input: {user_input}")
                response = await agent.process_message(user_input)
                print(f"\nTrainer: {response}\n")

            except KeyboardInterrupt:
                logger.info("Received keyboard interrupt")
                print("\n\n👋 Thanks for training with trAIner!")
                break
            except EOFError:
                logger.debug("Received EOF")
                break

    except Exception as e:
        logger.error(f"Error occurred: {e}", exc_info=True)
        print(f"\n❌ Error: {e}", file=sys.stderr)
        return 1

    logger.info("trAIner CLI shutting down")
    return 0


def main() -> int:
    """Entry point for the trainer CLI."""
    return asyncio.run(async_main())


if __name__ == "__main__":
    sys.exit(main())
