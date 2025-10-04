"""Basic usage example for trAIner."""

import asyncio

from trainer.agents import TrainerAgent


async def main():
    """Run basic trainer agent example."""
    # Initialize the trainer agent
    agent = TrainerAgent(model_name="gemini-2.0-flash-exp")
    await agent.initialize()

    # Example: Analyze a recent workout
    print("=== Workout Analysis Example ===")
    # workout_analysis = await agent.analyze_workout("12345")
    # print(f"Summary: {workout_analysis['summary']}")

    # Example: Chat with the trainer
    print("\n=== Chat Example ===")
    # response = await agent.process_message(
    #     "What should I focus on for my next training block?"
    # )
    # print(f"Trainer: {response}")

    # Example: Create a training plan
    print("\n=== Training Plan Example ===")
    # plan = await agent.create_training_plan(
    #     goal="Run a half marathon under 2 hours",
    #     weeks=12
    # )
    # print(f"Plan created: {plan['weeks']} weeks")


if __name__ == "__main__":
    asyncio.run(main())
