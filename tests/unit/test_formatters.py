"""Tests for formatting utilities."""

from trainer.utils.formatters import format_distance, format_duration, format_pace


def test_format_duration():
    """Test duration formatting."""
    assert format_duration(45) == "45s"
    assert format_duration(90) == "1m 30s"
    assert format_duration(3665) == "1h 1m 5s"
    assert format_duration(7200) == "2h"


def test_format_distance():
    """Test distance formatting."""
    assert format_distance(500) == "500 m"
    assert format_distance(1000) == "1.00 km"
    assert format_distance(5280) == "5.28 km"


def test_format_pace():
    """Test pace formatting."""
    # 5km in 25 minutes = 5:00 /km pace
    assert format_pace(5000, 1500, "km") == "5:00 /km"
    # 10km in 50 minutes = 5:00 /km pace
    assert format_pace(10000, 3000, "km") == "5:00 /km"
    # Handle zero distance
    assert format_pace(0, 1000, "km") == "N/A"
