"""Main trainer agent using Google ADK."""

import logging
import os
from typing import Any

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from trainer.tools import get_athlete_profile, get_athlete_stats, get_recent_activities
from trainer.utils.config import get_settings

logger = logging.getLogger(__name__)


class TrainerAgent:
    """AI personal trainer agent that uses Strava data to provide coaching."""

    def __init__(self, model_name: str = "gemini-2.0-flash-exp"):
        """Initialize the trainer agent.

        Args:
            model_name: The LLM to use for the agent
        """
        logger.info(f"Initializing TrainerAgent with model: {model_name}")

        # Set GOOGLE_API_KEY environment variable for Google ADK
        settings = get_settings()
        if settings.gemini_api_key:
            os.environ["GOOGLE_API_KEY"] = settings.gemini_api_key
        else:
            logger.warning("No API key found in GOOGLE_API_KEY or GEMINI_API_KEY")

        # Create the ADK agent with tools and instructions
        agent = Agent(
            name="personal_trainer",
            model=model_name,
            description=(
                "An AI personal trainer that analyzes Strava workout data "
                "and provides personalized coaching and training plans."
            ),
            instruction="""You are an expert personal trainer and coach specializing in \
endurance sports.

You have access to the athlete's Strava data through tools. Use this data to:
- Analyze workout performance and training patterns
- Provide personalized coaching feedback
- Identify areas for improvement
- Create structured training plans
- Answer questions about training, recovery, and performance

Be encouraging, data-driven, and specific in your recommendations. Consider:
- Training load and recovery
- Progressive overload principles
- Sport-specific training zones
- Injury prevention
- Goal-oriented planning

Always ground your advice in the actual data from Strava when available.""",
            tools=[get_athlete_profile, get_athlete_stats, get_recent_activities],
        )

        # Create the runner to manage agent execution
        self.session_service = InMemorySessionService()
        self.runner = Runner(app_name="trainer", agent=agent, session_service=self.session_service)
        self.user_id = "default_user"
        self.session_id = "default_session"
        logger.debug("TrainerAgent instance created with ADK Agent and Runner")

    async def process_message(self, message: str) -> str:
        """Process a user message and return a response.

        Args:
            message: User's message or question

        Returns:
            Agent's response
        """
        logger.debug(f"Processing message: {message[:50]}...")

        try:
            # Ensure session exists
            session = await self.session_service.get_session(
                app_name="trainer", user_id=self.user_id, session_id=self.session_id
            )
            if not session:
                await self.session_service.create_session(
                    app_name="trainer", user_id=self.user_id, session_id=self.session_id
                )

            # Convert message to Content object
            content = types.Content(role="user", parts=[types.Part(text=message)])

            # Use the runner to process the message
            response_parts = []
            async for event in self.runner.run_async(
                user_id=self.user_id,
                session_id=self.session_id,
                new_message=content,
            ):
                # Collect text from events with content
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        # Collect text parts (part.text might be None even if the attribute exists)
                        if hasattr(part, "text") and part.text:
                            response_parts.append(part.text)

            return "".join(response_parts) if response_parts else "No response generated"
        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
            return f"I encountered an error processing your message: {e}"

    async def analyze_workout(self, workout_id: str) -> dict[str, Any]:
        """Analyze a specific workout from Strava.

        Args:
            workout_id: Strava activity ID

        Returns:
            Analysis and recommendations
        """
        logger.info(f"Analyzing workout: {workout_id}")

        prompt = f"""Analyze the Strava activity with ID {workout_id}.

Please provide:
1. Summary of the workout (distance, duration, pace/power, heart rate)
2. Performance assessment relative to recent training
3. Strengths observed in this workout
4. Areas for improvement
5. Recovery recommendations
6. How this fits into their overall training plan"""

        response = await self.process_message(prompt)

        # Return structured response
        return {"workout_id": workout_id, "analysis": response, "status": "success"}

    async def create_training_plan(self, goal: str, weeks: int = 12) -> dict[str, Any]:
        """Create a personalized training plan.

        Args:
            goal: Training goal (e.g., "run a marathon", "improve cycling FTP")
            weeks: Number of weeks for the plan

        Returns:
            Training plan details
        """
        logger.info(f"Creating {weeks}-week training plan for goal: {goal}")

        prompt = f"""Create a {weeks}-week personalized training plan for the following goal: {goal}

Based on the athlete's recent Strava data:
1. Assess their current fitness level and training history
2. Design a progressive training plan with weekly structure
3. Include specific workouts (easy runs, tempo, intervals, long runs/rides, etc.)
4. Build in appropriate recovery
5. Progressively increase training load
6. Taper if relevant for the goal
7. Provide weekly guidance and focus areas

Format the plan with week-by-week breakdown."""

        response = await self.process_message(prompt)

        return {"goal": goal, "weeks": weeks, "plan": response, "status": "success"}

    async def run_interactive(self) -> None:
        """Run the agent in interactive mode with user input loop."""
        logger.info("Starting interactive mode")
        print("\n🏃 trAIner - Your AI Personal Trainer")
        print("Connected to Strava data via MCP")
        print("Enter your question below.")
        print("Type 'quit' or 'exit' to stop.\n")

        while True:
            try:
                user_input = input("💪> ").strip()

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
