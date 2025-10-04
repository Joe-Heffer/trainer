"""Training plan data models."""

from datetime import date

from pydantic import BaseModel, Field


class TrainingSession(BaseModel):
    """A single training session in a plan."""

    day: str  # e.g., "Monday", "Day 1"
    type: str  # e.g., "Easy Run", "Interval Training", "Rest"
    description: str
    duration_minutes: int | None = None
    distance_km: float | None = None
    intensity: str  # e.g., "Low", "Moderate", "High"
    notes: str | None = None


class TrainingWeek(BaseModel):
    """A week in the training plan."""

    week_number: int
    start_date: date | None = None
    focus: str  # e.g., "Base Building", "Speed Work", "Recovery"
    sessions: list[TrainingSession]
    total_distance_km: float | None = None
    weekly_notes: str | None = None


class TrainingPlan(BaseModel):
    """Complete training plan."""

    goal: str
    start_date: date
    end_date: date
    weeks: list[TrainingWeek]
    athlete_level: str = Field(
        ..., description="Athlete fitness level: beginner, intermediate, advanced"
    )
    notes: str | None = Field(None, description="General plan notes and guidelines")
