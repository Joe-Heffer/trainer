"""Main trainer agent using Google ADK."""

import logging
from typing import Any

import google.genai

logger = logging.getLogger(__name__)


class TrainerAgent:
    """AI personal trainer agent that uses Strava data to provide coaching."""

    def __init__(self, model_name: str = "gemini-2.0-flash-exp"):
        """Initialize the trainer agent.

        Args:
            model_name: The LLM to use for the agent
        """
        logger.info(f"Initializing TrainerAgent with model: {model_name}")
        self.client = google.genai.Client()
        self.model_name = model_name
        self.agent = None
        logger.debug("TrainerAgent instance created")

    async def initialize(self) -> None:
        """Initialize the agent with tools and configuration."""
        logger.info("Initializing agent with tools and configuration")
        # TODO: Connect Strava MCP tool
        # TODO: Define agent instructions and behavior
        raise NotImplementedError

    async def process_message(self, message: str) -> str:
        """Process a user message and return a response.

        Args:
            message: User's message or question

        Returns:
            Agent's response
        """
        logger.debug(f"Processing message: {message[:50]}...")
        # TODO: Implement message processing with agent
        raise NotImplementedError

    async def analyze_workout(self, workout_id: str) -> dict[str, Any]:
        """Analyze a specific workout from Strava.

        Args:
            workout_id: Strava activity ID

        Returns:
            Analysis and recommendations
        """
        logger.info(f"Analyzing workout: {workout_id}")
        # TODO: Implement workout analysis
        raise NotImplementedError

    async def create_training_plan(self, goal: str, weeks: int = 12) -> dict[str, Any]:
        """Create a personalized training plan.

        Args:
            goal: Training goal (e.g., "run a marathon", "improve cycling FTP")
            weeks: Number of weeks for the plan

        Returns:
            Training plan details
        """
        logger.info(f"Creating {weeks}-week training plan for goal: {goal}")
        # TODO: Implement training plan generation
        raise NotImplementedError

    async def run_interactive(self) -> None:
        """Run the agent in interactive mode with user input loop."""
        logger.info("Starting interactive mode")
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
                response = await self.process_message(user_input)
                print(f"\nTrainer: {response}\n")

            except KeyboardInterrupt:
                logger.info("Received keyboard interrupt")
                print("\n\n👋 Thanks for training with trAIner!")
                break
            except EOFError:
                logger.debug("Received EOF")
                break
