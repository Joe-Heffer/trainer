"""Integration tests for trainer agent."""

from unittest.mock import patch

import pytest
from trainer.agents.trainer_agent import TrainerAgent


@pytest.mark.asyncio
async def test_trainer_agent_initialization(mock_genai_client):
    """Test that trainer agent can be initialized."""
    with patch("trainer.agents.trainer_agent.genai.Client", return_value=mock_genai_client):
        agent = TrainerAgent()
        assert agent.model_name == "gemini-2.0-flash-exp"
        await agent.initialize()


@pytest.mark.asyncio
@pytest.mark.skip(reason="Requires Strava MCP server running")
async def test_analyze_workout_integration():
    """Test workout analysis with real Strava data."""
    # This test requires real API keys and running MCP server
    # Only run manually with: pytest -m "not skip"
    agent = TrainerAgent()
    await agent.initialize()
    # analysis = await agent.analyze_workout("12345")
    # assert "summary" in analysis
