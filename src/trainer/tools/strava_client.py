"""Strava MCP client integration."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class StravaClient:
    """Client for interacting with Strava via MCP."""

    def __init__(self, mcp_server_url: str | None = None):
        """Initialize Strava MCP client.

        Args:
            mcp_server_url: URL of the Strava MCP server
        """
        logger.info(f"Initializing StravaClient with URL: {mcp_server_url}")
        self.mcp_server_url = mcp_server_url
        # TODO: Initialize MCP connection
        logger.debug("StravaClient instance created")

    async def get_athlete_stats(self) -> dict[str, Any]:
        """Get athlete statistics from Strava.

        Returns:
            Athlete stats including recent activities
        """
        logger.info("Fetching athlete statistics from Strava")
        # TODO: Implement via MCP
        raise NotImplementedError

    async def get_recent_activities(self, limit: int = 30) -> list[dict[str, Any]]:
        """Get recent activities from Strava.

        Args:
            limit: Maximum number of activities to retrieve

        Returns:
            List of recent activities
        """
        logger.info(f"Fetching {limit} recent activities from Strava")
        # TODO: Implement via MCP
        raise NotImplementedError

    async def get_activity_details(self, activity_id: str) -> dict[str, Any]:
        """Get detailed information about a specific activity.

        Args:
            activity_id: Strava activity ID

        Returns:
            Detailed activity data
        """
        logger.info(f"Fetching details for activity: {activity_id}")
        # TODO: Implement via MCP
        raise NotImplementedError
