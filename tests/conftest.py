"""Pytest configuration and fixtures."""

import os
import pytest
from unittest.mock import AsyncMock, MagicMock, patch


@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    """Mock environment variables for all tests."""
    monkeypatch.setenv("GEMINI_API_KEY", "test-api-key-12345")
    monkeypatch.setenv("STRAVA_MCP_URL", "http://localhost:3000")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")


@pytest.fixture
def mock_genai_client():
    """Mock Google GenAI client."""
    with patch("google.genai.Client") as mock_client_class:
        mock_instance = MagicMock()
        mock_client_class.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def mock_strava_client():
    """Mock Strava MCP client for testing."""
    mock_client = AsyncMock()
    mock_client.get_athlete_stats.return_value = {
        "recent_run_totals": {"count": 10, "distance": 50000},
        "all_time_totals": {"count": 100, "distance": 500000},
    }
    return mock_client


@pytest.fixture
def sample_workout_data():
    """Sample workout data for testing."""
    return {
        "id": "12345",
        "name": "Morning Run",
        "type": "Run",
        "start_date": "2025-10-01T06:00:00Z",
        "distance": 5000.0,
        "duration": 1800,
        "elevation_gain": 50.0,
        "average_heartrate": 145.0,
        "max_heartrate": 165.0,
        "average_speed": 2.78,
        "calories": 350.0,
    }
