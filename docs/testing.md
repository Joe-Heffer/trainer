# Testing Guide

## Overview

trAIner uses pytest for testing with automatic mocking of external dependencies (Google Gemini API, Strava MCP).

## Running Tests

### Run All Tests
```bash
pytest
```

### Run with Coverage
```bash
pytest --cov=trainer --cov-report=html
# Open htmlcov/index.html to view coverage report
```

### Run Specific Test Types
```bash
# Unit tests only
pytest tests/unit

# Integration tests only
pytest tests/integration

# Skip integration tests
pytest -m "not integration"
```

### Run Specific Test File
```bash
pytest tests/unit/test_formatters.py -v
```

## Test Structure

```
tests/
├── conftest.py           # Shared fixtures and configuration
├── unit/                 # Unit tests (fast, no external deps)
│   ├── test_formatters.py
│   └── test_models.py
└── integration/          # Integration tests (may require external services)
    └── test_agent.py
```

## Fixtures

### Auto-Mocked (Applied to All Tests)

**mock_env_vars**
- Automatically sets test environment variables
- No need for real API keys in tests
- Values:
  - `GEMINI_API_KEY=test-api-key-12345`
  - `STRAVA_MCP_URL=http://localhost:3000`
  - `LOG_LEVEL=DEBUG`

### Optional Fixtures

**mock_genai_client**
```python
def test_with_mocked_gemini(mock_genai_client):
    # Google GenAI client is mocked
    agent = TrainerAgent()
```

**mock_strava_client**
```python
def test_with_mocked_strava(mock_strava_client):
    # Strava MCP client is mocked
    stats = await mock_strava_client.get_athlete_stats()
```

**sample_workout_data**
```python
def test_with_sample_data(sample_workout_data):
    workout = Workout(**sample_workout_data)
```

## Writing Tests

### Unit Test Example

```python
# tests/unit/test_my_feature.py
import pytest
from trainer.utils.formatters import format_duration


def test_format_duration():
    """Test duration formatting."""
    assert format_duration(3661) == "1h 1m 1s"
    assert format_duration(90) == "1m 30s"
    assert format_duration(45) == "45s"
```

### Async Test Example

```python
import pytest
from trainer.agents.trainer_agent import TrainerAgent


@pytest.mark.asyncio
async def test_agent_initialization(mock_genai_client):
    """Test agent initializes correctly."""
    agent = TrainerAgent()
    await agent.initialize()
    assert agent.client is not None
```

### Integration Test Example

```python
import pytest


@pytest.mark.integration
@pytest.mark.skip(reason="Requires MCP server running")
async def test_real_strava_connection():
    """Test with real Strava MCP server."""
    # This test would need real API keys
    # Only run manually when testing integration
    pass
```

## Mocking Best Practices

### 1. Mock External Services

Always mock API calls to avoid:
- Rate limits
- Network failures
- Need for real credentials
- Slow tests

```python
from unittest.mock import patch, AsyncMock

@pytest.mark.asyncio
async def test_analyze_workout():
    mock_client = AsyncMock()
    mock_client.get_activity_details.return_value = {...}

    with patch("trainer.tools.strava_client.StravaClient", return_value=mock_client):
        # Your test code
        pass
```

### 2. Use Fixtures for Reusable Mocks

Add to `tests/conftest.py`:
```python
@pytest.fixture
def mock_training_plan():
    return TrainingPlan(
        goal="Run 5K under 25 minutes",
        weeks=8,
        workouts=[...]
    )
```

### 3. Test Edge Cases

```python
def test_format_duration_edge_cases():
    assert format_duration(0) == "0s"
    assert format_duration(86400) == "24h 0m 0s"

    with pytest.raises(ValueError):
        format_duration(-1)
```

## CI/CD Testing

### GitHub Actions

Tests run automatically on:
- Push to `main` branch
- Pull requests

See `.github/workflows/ci.yml` for configuration.

### Local Pre-Commit Checks

Before committing:
```bash
# Format code
ruff format .

# Check linting
ruff check .

# Type check
mypy src/trainer

# Run tests
pytest

# All checks with coverage
ruff format . && ruff check . && mypy src/trainer && pytest --cov=trainer
```

## Troubleshooting

### Import Errors

**Error**: `ModuleNotFoundError: No module named 'trainer'`

**Solution**: Install package in editable mode:
```bash
pip install -e ".[dev]"
```

### Async Test Failures

**Error**: `RuntimeError: Event loop is closed`

**Solution**: Ensure test is marked with `@pytest.mark.asyncio`:
```python
@pytest.mark.asyncio
async def test_my_async_function():
    pass
```

### Fixture Not Found

**Error**: `fixture 'my_fixture' not found`

**Solution**: Check fixture is defined in:
1. Same test file
2. `tests/conftest.py`
3. Parent directory's `conftest.py`

### API Key Errors in Tests

**Error**: `ValueError: Missing key inputs argument!`

**Solution**: The `mock_env_vars` fixture should auto-apply. Verify:
```python
# In conftest.py, fixture should have autouse=True
@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-api-key-12345")
```

## Code Coverage

### View Coverage Report

```bash
pytest --cov=trainer --cov-report=html
open htmlcov/index.html  # macOS/Linux
start htmlcov/index.html  # Windows
```

### Coverage Goals

- **Overall**: >80%
- **Core Logic**: >90% (agents, models)
- **Utils**: >85%
- **Integration Tests**: Can be lower (external deps)

### Excluding from Coverage

For code that doesn't need testing:
```python
def debug_only_function():  # pragma: no cover
    print("Debug info")
```

## Related Documentation

- [CONTRIBUTING.md](../CONTRIBUTING.md)
- [Architecture Overview](architecture.md)
- [Installation Guide](installation.md)
