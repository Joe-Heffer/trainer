"""Strava MCP client integration."""

from typing import Any


class StravaClient:
    """Client for interacting with Strava via MCP."""

    def __init__(self, mcp_server_url: str | None = None):
        """Initialize Strava MCP client.

        Args:
            mcp_server_url: URL of the Strava MCP server
        """
        self.mcp_server_url = mcp_server_url
        # TODO: Initialize MCP connection

    async def get_athlete_stats(self) -> dict[str, Any]:
        """Get athlete statistics from Strava.

        Returns:
            Athlete stats including recent activities
        """
        # TODO: Implement via MCP
        raise NotImplementedError

    async def get_recent_activities(self, limit: int = 30) -> list[dict[str, Any]]:
        """Get recent activities from Strava.

        Args:
            limit: Maximum number of activities to retrieve

        Returns:
            List of recent activities
        """
        # TODO: Implement via MCP
        raise NotImplementedError

    async def get_activity_details(self, activity_id: str) -> dict[str, Any]:
        """Get detailed information about a specific activity.

        Args:
            activity_id: Strava activity ID

        Returns:
            Detailed activity data
        """
        # TODO: Implement via MCP
        raise NotImplementedError
