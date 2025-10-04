"""Formatting utilities for fitness data."""


def format_duration(seconds: int) -> str:
    """Format duration in seconds to human-readable string.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted string (e.g., "1h 23m 45s")
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if secs > 0 or not parts:
        parts.append(f"{secs}s")

    return " ".join(parts)


def format_distance(meters: float) -> str:
    """Format distance in meters to human-readable string.

    Args:
        meters: Distance in meters

    Returns:
        Formatted string (e.g., "5.2 km" or "850 m")
    """
    if meters >= 1000:
        km = meters / 1000
        return f"{km:.2f} km"
    return f"{int(meters)} m"


def format_pace(meters: float, seconds: int, unit: str = "km") -> str:
    """Format pace for running/walking activities.

    Args:
        meters: Distance in meters
        seconds: Duration in seconds
        unit: Unit for pace ("km" or "mi")

    Returns:
        Formatted pace string (e.g., "5:30 /km")
    """
    if meters == 0:
        return "N/A"

    # Calculate pace per km or mile
    distance_in_unit = meters / 1000 if unit == "km" else meters / 1609.34
    pace_seconds = seconds / distance_in_unit if distance_in_unit > 0 else 0

    pace_minutes = int(pace_seconds // 60)
    pace_secs = int(pace_seconds % 60)

    return f"{pace_minutes}:{pace_secs:02d} /{unit}"
