"""Main entry point for the trainer CLI."""

import asyncio
import sys

from trainer.agents.trainer_agent import TrainerAgent


async def async_main() -> int:
    """Async main function that runs the trainer agent."""
    print("🏃 trAIner - Your AI Personal Trainer")
    print("=" * 40)

    agent = TrainerAgent()

    try:
        await agent.initialize()
        print("\nAgent initialized. Type 'quit' or 'exit' to stop.\n")

        while True:
            try:
                user_input = input("You: ").strip()

                if user_input.lower() in ("quit", "exit", "q"):
                    print("\n👋 Thanks for training with trAIner!")
                    break

                if not user_input:
                    continue

                response = await agent.process_message(user_input)
                print(f"\nTrainer: {response}\n")

            except KeyboardInterrupt:
                print("\n\n👋 Thanks for training with trAIner!")
                break
            except EOFError:
                break

    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        return 1

    return 0


def main() -> int:
    """Entry point for the trainer CLI."""
    return asyncio.run(async_main())


if __name__ == "__main__":
    sys.exit(main())
