"""Example of using Strava MCP integration."""

import asyncio

from trainer.tools import StravaClient


async def main():
    """Demonstrate Strava MCP client usage."""
    # Initialize Strava client
    client = StravaClient()

    # Get athlete statistics
    print("=== Athlete Stats ===")
    # stats = await client.get_athlete_stats()
    # print(f"Total runs: {stats['recent_run_totals']['count']}")
    # print(f"Total distance: {stats['recent_run_totals']['distance']} meters")

    # Get recent activities
    print("\n=== Recent Activities ===")
    # activities = await client.get_recent_activities(limit=5)
    # for activity in activities:
    #     print(f"- {activity['name']} ({activity['type']}): {activity['distance']}m")

    # Get detailed activity information
    print("\n=== Activity Details ===")
    # activity = await client.get_activity_details("12345")
    # print(f"Activity: {activity['name']}")
    # print(f"Duration: {activity['duration']} seconds")
    # print(f"Average HR: {activity.get('average_heartrate', 'N/A')}")


if __name__ == "__main__":
    asyncio.run(main())
