"""Strava integration using MCP (Model Context Protocol)."""

import asyncio
import logging
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from trainer.utils.config import get_settings

logger = logging.getLogger(__name__)

# Global MCP client and session - kept alive for reuse
_mcp_client_context = None
_mcp_session_context = None
_mcp_session: ClientSession | None = None
_mcp_lock = asyncio.Lock()  # Lock to prevent concurrent MCP calls


async def close_mcp_session() -> None:
    """Close the MCP session and cleanup resources."""
    global _mcp_client_context, _mcp_session_context, _mcp_session

    if _mcp_session_context:
        try:
            await _mcp_session_context.__aexit__(None, None, None)
        except Exception:
            pass
        _mcp_session_context = None

    if _mcp_client_context:
        try:
            await _mcp_client_context.__aexit__(None, None, None)
        except Exception:
            pass
        _mcp_client_context = None

    _mcp_session = None
    logger.info("MCP session closed")


async def _get_mcp_session() -> ClientSession:
    """Get or create MCP client session for Strava server.

    Returns:
        Active MCP client session
    """
    global _mcp_client_context, _mcp_session_context, _mcp_session

    if _mcp_session is not None:
        return _mcp_session

    # Get Strava MCP server path from environment
    settings = get_settings()
    strava_mcp_path = settings.strava_mcp_path
    if not strava_mcp_path:
        raise ValueError(
            "STRAVA_MCP_PATH not configured. Set the path to the strava-mcp dist/server.js file."
        )

    logger.info(f"Connecting to Strava MCP server: {strava_mcp_path}")

    # Create server parameters for the Strava MCP server
    server_params = StdioServerParameters(
        command="node",
        args=[strava_mcp_path],
        env=None,  # Server reads from its own .env file
    )

    # Create and store the session - keep context managers active
    _mcp_client_context = stdio_client(server_params)
    read, write = await _mcp_client_context.__aenter__()

    _mcp_session_context = ClientSession(read, write)
    _mcp_session = await _mcp_session_context.__aenter__()
    await _mcp_session.initialize()

    logger.info("MCP session initialized successfully")
    return _mcp_session


async def get_recent_activities(per_page: int) -> dict[str, Any]:
    """Get recent workout activities from Strava.

    Retrieves the athlete's most recent activities with details including:
    - Activity type (run, ride, swim, etc.)
    - Distance and duration
    - Pace/speed metrics
    - Heart rate data if available
    - Elevation gain
    - Timestamp

    Args:
        per_page: Number of activities to retrieve per page (max: 200)

    Returns:
        Dictionary with status and list of recent activities, or error message
    """
    logger.info(f"Tool called: get_recent_activities(per_page={per_page})")

    async with _mcp_lock:
        try:
            session = await _get_mcp_session()

            # Call the MCP tool
            result = await session.call_tool(
                "get-recent-activities",
                arguments={"perPage": per_page},
            )

            return {
                "status": "success",
                "data": result.content,
            }
        except Exception as e:
            logger.error(f"Error fetching recent activities: {e}")
            return {
                "status": "error",
                "error_message": f"Failed to retrieve recent activities: {str(e)}",
            }


async def get_athlete_profile() -> dict[str, Any]:
    """Get the authenticated athlete's profile information.

    Returns:
        Dictionary with status and athlete profile data, or error message
    """
    logger.info("Tool called: get_athlete_profile")

    async with _mcp_lock:
        try:
            session = await _get_mcp_session()

            result = await session.call_tool("get-athlete-profile", arguments={})

            return {
                "status": "success",
                "data": result.content,
            }
        except Exception as e:
            logger.error(f"Error fetching athlete profile: {e}")
            return {
                "status": "error",
                "error_message": f"Failed to retrieve athlete profile: {str(e)}",
            }


async def get_athlete_stats(athlete_id: int) -> dict[str, Any]:
    """Get athlete statistics and recent performance data from Strava.

    Retrieves comprehensive statistics about the athlete including:
    - Recent activity summary (last 4 weeks)
    - Year-to-date totals
    - All-time totals
    - Training volume metrics
    - Performance trends

    Args:
        athlete_id: The unique Strava athlete ID (obtain from get_athlete_profile first)

    Returns:
        Dictionary with status and athlete statistics data, or error message
    """
    logger.info(f"Tool called: get_athlete_stats(athlete_id={athlete_id})")

    async with _mcp_lock:
        try:
            session = await _get_mcp_session()

            result = await session.call_tool(
                "get-athlete-stats", arguments={"athleteId": athlete_id}
            )

            return {
                "status": "success",
                "data": result.content,
            }
        except Exception as e:
            logger.error(f"Error fetching athlete stats: {e}")
            return {
                "status": "error",
                "error_message": f"Failed to retrieve athlete statistics: {str(e)}",
            }


async def get_activity_details(activity_id: str) -> dict[str, Any]:
    """Get detailed information about a specific Strava activity.

    Retrieves comprehensive details for a single workout including:
    - Full activity metrics (distance, duration, pace, speed)
    - Heart rate zones and analysis
    - Power data (for cycling/running with power meter)
    - Elevation profile
    - Splits and laps
    - GPS data and route

    Args:
        activity_id: The Strava activity ID to analyze

    Returns:
        Dictionary with status and detailed activity data, or error message
    """
    logger.info(f"Tool called: get_activity_details(activity_id={activity_id})")

    async with _mcp_lock:
        try:
            session = await _get_mcp_session()

            result = await session.call_tool(
                "get-activity-details",
                arguments={"activityId": activity_id},
            )

            return {
                "status": "success",
                "data": result.content,
            }
        except Exception as e:
            logger.error(f"Error fetching activity details for {activity_id}: {e}")
            return {
                "status": "error",
                "error_message": f"Failed to retrieve activity details: {str(e)}",
            }


async def list_athlete_clubs() -> dict[str, Any]:
    """List all clubs the athlete has joined.

    Returns:
        Dictionary with status and list of clubs, or error message
    """
    logger.info("Tool called: list_athlete_clubs")

    async with _mcp_lock:
        try:
            session = await _get_mcp_session()

            result = await session.call_tool("list-athlete-clubs", arguments={})

            return {
                "status": "success",
                "data": result.content,
            }
        except Exception as e:
            logger.error(f"Error fetching athlete clubs: {e}")
            return {
                "status": "error",
                "error_message": f"Failed to retrieve athlete clubs: {str(e)}",
            }


async def get_segment(segment_id: str) -> dict[str, Any]:
    """Get details for a specific Strava segment.

    Args:
        segment_id: The Strava segment ID

    Returns:
        Dictionary with status and segment details, or error message
    """
    logger.info(f"Tool called: get_segment(segment_id={segment_id})")

    async with _mcp_lock:
        try:
            session = await _get_mcp_session()

            result = await session.call_tool(
                "get-segment",
                arguments={"segmentId": segment_id},
            )

            return {
                "status": "success",
                "data": result.content,
            }
        except Exception as e:
            logger.error(f"Error fetching segment {segment_id}: {e}")
            return {
                "status": "error",
                "error_message": f"Failed to retrieve segment: {str(e)}",
            }
