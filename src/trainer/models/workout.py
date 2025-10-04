"""Workout data models."""

from datetime import datetime
from pydantic import BaseModel, Field


class Workout(BaseModel):
    """Represents a workout/activity from Strava."""

    id: str
    name: str
    type: str  # e.g., "Run", "Ride", "Swim"
    start_date: datetime
    distance: float = Field(..., description="Distance in meters")
    duration: int = Field(..., description="Duration in seconds")
    elevation_gain: float | None = Field(None, description="Elevation gain in meters")
    average_heartrate: float | None = None
    max_heartrate: float | None = None
    average_speed: float | None = Field(None, description="Speed in m/s")
    calories: float | None = None


class WorkoutAnalysis(BaseModel):
    """Analysis and feedback for a workout."""

    workout_id: str
    summary: str = Field(..., description="Brief summary of the workout")
    strengths: list[str] = Field(default_factory=list)
    areas_for_improvement: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    effort_rating: int = Field(..., ge=1, le=10, description="Perceived effort (1-10)")
    recovery_advice: str | None = None
