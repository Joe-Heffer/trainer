"""Tests for data models."""

from trainer.models import Workout, WorkoutAnalysis


def test_workout_model(sample_workout_data):
    """Test Workout model validation."""
    workout = Workout(**sample_workout_data)
    assert workout.id == "12345"
    assert workout.name == "Morning Run"
    assert workout.distance == 5000.0


def test_workout_analysis_model():
    """Test WorkoutAnalysis model."""
    analysis = WorkoutAnalysis(
        workout_id="12345",
        summary="Great run with consistent pace",
        strengths=["Good heart rate control", "Steady pace"],
        areas_for_improvement=["Could increase cadence"],
        recommendations=["Try interval training next week"],
        effort_rating=7,
        recovery_advice="Easy run tomorrow",
    )
    assert analysis.effort_rating == 7
    assert len(analysis.strengths) == 2
