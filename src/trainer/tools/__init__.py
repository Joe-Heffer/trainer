"""MCP tools and integrations."""

from .strava_mcp import (
    close_mcp_session,
    get_activity_details,
    get_athlete_profile,
    get_athlete_stats,
    get_recent_activities,
    get_segment,
    list_athlete_clubs,
)

__all__ = [
    "get_athlete_profile",
    "get_athlete_stats",
    "get_recent_activities",
    "get_activity_details",
    "list_athlete_clubs",
    "get_segment",
    "close_mcp_session",
]
