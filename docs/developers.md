# Developer Guide

Comprehensive guide for developers working on trAIner.

## Table of Contents

- [Development Environment Setup](#development-environment-setup)
- [Project Architecture](#project-architecture)
- [Development Workflow](#development-workflow)
- [Code Quality](#code-quality)
- [Testing](#testing)
- [Debugging](#debugging)
- [Common Tasks](#common-tasks)
- [Troubleshooting](#troubleshooting)

## Development Environment Setup

### Prerequisites

- **Python 3.13+**: [Download](https://www.python.org/downloads/)
- **Git**: [Download](https://git-scm.com/downloads)
- **Node.js 18+**: For MCP server ([Download](https://nodejs.org/))
- **Google Gemini API Key**: [Get one](https://aistudio.google.com/app/apikey)
- **Strava API Access**: [Register app](https://www.strava.com/settings/api)

### Initial Setup

```bash
# Clone repository
git clone https://github.com/yourusername/trainer.git
cd trainer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Set up pre-commit hooks
pre-commit install

# Set up environment
cp .env.example .env
# Edit .env with your credentials

# Verify installation
pytest
```

### IDE Setup

**VS Code** (recommended):
```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "python.testing.pytestEnabled": true,
  "python.linting.ruffEnabled": true,
  "editor.formatOnSave": true,
  "python.formatting.provider": "none",
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  }
}
```

**PyCharm**:
- Mark `src` as Sources Root
- Configure pytest as test runner
- Enable ruff for formatting and linting

## Project Architecture

### Directory Structure

```
trainer/
├── .github/
│   ├── workflows/         # CI/CD workflows
│   └── dependabot.yml     # Dependency updates
├── docs/                  # Documentation
├── examples/              # Example scripts
├── src/trainer/
│   ├── agents/            # AI agent implementations
│   │   └── trainer_agent.py
│   ├── models/            # Pydantic data models
│   │   ├── workout.py
│   │   └── training_plan.py
│   ├── tools/             # External integrations
│   │   └── strava_client.py
│   ├── utils/             # Utilities
│   │   ├── config.py
│   │   └── formatters.py
│   ├── __init__.py
│   └── __main__.py        # CLI entry point
├── tests/
│   ├── conftest.py        # Test fixtures
│   ├── unit/              # Unit tests
│   └── integration/       # Integration tests
├── .env.example           # Environment template
├── mcp_config.json        # MCP server config
├── pyproject.toml         # Project metadata
└── README.md
```

### Key Components

**Agents** (`src/trainer/agents/`)
- Use Google ADK for agentic AI
- Integrate with tools (Strava, etc.)
- Handle conversation and task planning

**Models** (`src/trainer/models/`)
- Pydantic v2 for data validation
- Type-safe data structures
- Automatic serialization

**Tools** (`src/trainer/tools/`)
- MCP client integrations
- External API wrappers
- Async I/O operations

**Utils** (`src/trainer/utils/`)
- Configuration management
- Formatting helpers
- Shared utilities

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feat/your-feature-name
```

Branch naming:
- `feat/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation
- `test/` - Test improvements
- `refactor/` - Code refactoring

### 2. Make Changes

Follow these principles:

**Type Safety**
```python
# Good: Full type hints
async def analyze_workout(workout_id: str) -> WorkoutAnalysis:
    ...

# Bad: Missing types
async def analyze_workout(workout_id):
    ...
```

**Async/Await**
```python
# Good: Async for I/O
async def fetch_data(url: str) -> dict[str, Any]:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

# Bad: Blocking I/O
def fetch_data(url: str) -> dict[str, Any]:
    response = requests.get(url)
    return response.json()
```

**Error Handling**
```python
# Good: Specific exceptions
try:
    workout = await client.get_activity_details(activity_id)
except httpx.HTTPError as e:
    logger.error(f"Failed to fetch workout: {e}")
    raise WorkoutFetchError(f"Could not fetch activity {activity_id}") from e

# Bad: Bare except
try:
    workout = await client.get_activity_details(activity_id)
except:
    pass
```

### 3. Write Tests

For every new function, write tests:

```python
# tests/unit/test_my_feature.py
import pytest
from trainer.my_module import my_function


def test_my_function_success():
    """Test normal operation."""
    result = my_function("input")
    assert result == "expected"


def test_my_function_edge_case():
    """Test edge cases."""
    with pytest.raises(ValueError):
        my_function(None)
```

### 4. Run Quality Checks

**Automatic checks with pre-commit** (recommended):

Pre-commit hooks automatically run on every commit:
- Format code with ruff
- Lint code with ruff
- Type check with mypy
- Check for common issues (trailing whitespace, merge conflicts, etc.)

```bash
# Hooks run automatically on git commit
git commit -m "feat: my changes"

# Run manually on all files
pre-commit run --all-files

# Skip hooks if needed (not recommended)
git commit --no-verify
```

**Manual checks**:

```bash
# Format code
ruff format .

# Check linting
ruff check .

# Type check
mypy src/trainer

# Run tests
pytest

# Check coverage
pytest --cov=trainer --cov-report=term-missing
```

### 5. Commit Changes

Use conventional commits:

```bash
git add .
git commit -m "feat: add workout comparison feature

- Add compare_workouts() method to TrainerAgent
- Include statistical analysis of pace and HR
- Add tests for comparison logic
"
```

### 6. Push and Create PR

```bash
git push origin feat/your-feature-name
```

Open PR with:
- Clear title and description
- Link to related issues
- Screenshots if applicable
- Checklist of changes

## Code Quality

### Linting with Ruff

Configuration in `pyproject.toml`:
```toml
[tool.ruff]
line-length = 100
target-version = "py313"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]
```

Common issues:
```python
# E501: Line too long
# Fix: Break into multiple lines
result = some_function(
    long_parameter_1,
    long_parameter_2,
    long_parameter_3
)

# F401: Unused import
# Fix: Remove unused imports

# I001: Import not sorted
# Fix: Run `ruff check . --fix`
```

### Type Checking with Mypy

Configuration in `pyproject.toml`:
```toml
[tool.mypy]
python_version = "3.13"
strict = true
```

Common issues:
```python
# error: Function is missing a return type annotation
# Fix: Add return type
def get_name() -> str:
    return "name"

# error: Need type annotation for variable
# Fix: Add type hint
workouts: list[Workout] = []
```

### Code Style

**Docstrings** (Google style):
```python
def format_pace(speed: float, metric: bool = True) -> str:
    """Format speed as pace.

    Args:
        speed: Speed in m/s
        metric: Use metric (min/km) vs imperial (min/mi)

    Returns:
        Formatted pace string (e.g., "5:30/km")

    Raises:
        ValueError: If speed is negative or zero
    """
    if speed <= 0:
        raise ValueError("Speed must be positive")
    # Implementation
```

**Naming Conventions**:
- `snake_case` for functions and variables
- `PascalCase` for classes
- `UPPER_CASE` for constants
- Private: prefix with `_`

**Imports**:
```python
# Standard library
import os
from datetime import datetime
from typing import Any

# Third-party
import httpx
from pydantic import BaseModel

# Local
from trainer.models.workout import Workout
from trainer.utils.formatters import format_duration
```

## Testing

See [Testing Guide](testing.md) for comprehensive details.

### Quick Reference

```bash
# Run all tests
pytest

# Run specific test
pytest tests/unit/test_formatters.py::test_format_duration -v

# Run with coverage
pytest --cov=trainer --cov-report=html

# Run only unit tests
pytest tests/unit

# Skip integration tests
pytest -m "not integration"

# Run tests matching pattern
pytest -k "test_format"

# Verbose output
pytest -vv

# Stop on first failure
pytest -x

# Run last failed tests
pytest --lf
```

### Writing Effective Tests

**Structure**: Arrange-Act-Assert
```python
def test_workout_pace_calculation():
    # Arrange
    workout = Workout(distance=5000, duration=1500, ...)

    # Act
    pace = calculate_pace(workout)

    # Assert
    assert pace == "5:00/km"
```

**Fixtures**: Reuse common setup
```python
@pytest.fixture
def sample_workout():
    return Workout(
        id="123",
        distance=5000,
        duration=1500,
        ...
    )

def test_with_fixture(sample_workout):
    assert sample_workout.distance == 5000
```

**Parametrize**: Test multiple inputs
```python
@pytest.mark.parametrize("duration,expected", [
    (60, "1m 0s"),
    (3661, "1h 1m 1s"),
    (45, "45s"),
])
def test_format_duration(duration, expected):
    assert format_duration(duration) == expected
```

## Debugging

### Using pytest with debugger

```bash
# Drop into debugger on failure
pytest --pdb

# Drop into debugger at start of test
pytest --trace
```

### Using print debugging (dev only)

```python
# For quick debugging (remove before commit)
print(f"DEBUG: workout={workout}")

# Better: Use logging
import logging
logger = logging.getLogger(__name__)
logger.debug(f"Processing workout: {workout.id}")
```

### Using VS Code debugger

Create `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Current Test",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": ["${file}", "-v"],
      "console": "integratedTerminal"
    }
  ]
}
```

## Common Tasks

### Adding a New Model

```python
# src/trainer/models/new_model.py
from pydantic import BaseModel, Field

class NewModel(BaseModel):
    """Description of model."""

    id: str
    name: str
    value: float = Field(..., ge=0)

# tests/unit/test_new_model.py
def test_new_model():
    model = NewModel(id="1", name="test", value=10.0)
    assert model.value == 10.0
```

### Adding a New Tool

```python
# src/trainer/tools/new_tool.py
class NewToolClient:
    """Client for new external service."""

    async def fetch_data(self) -> dict[str, Any]:
        """Fetch data from service."""
        # Implementation
        pass

# tests/unit/test_new_tool.py
@pytest.mark.asyncio
async def test_new_tool():
    client = NewToolClient()
    data = await client.fetch_data()
    assert data is not None
```

### Adding a New Agent Method

```python
# src/trainer/agents/trainer_agent.py
class TrainerAgent:
    async def new_feature(self, param: str) -> Result:
        """New agent capability."""
        # Use tools
        data = await self.strava_client.get_data()

        # Use AI
        response = await self.agent.generate(prompt)

        return Result(...)

# tests/integration/test_agent.py
@pytest.mark.asyncio
async def test_new_feature(mock_genai_client):
    agent = TrainerAgent()
    result = await agent.new_feature("test")
    assert result is not None
```

## Troubleshooting

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'trainer'`

**Solution**:
```bash
pip install -e .
```

### Test Failures

**Problem**: `ValueError: Missing key inputs argument!`

**Solution**: Check `tests/conftest.py` has `mock_env_vars` fixture with `autouse=True`

### Type Check Errors

**Problem**: `error: Incompatible return value type`

**Solution**: Fix type annotations to match actual return type

### Linting Errors

**Problem**: `Ruff check failed`

**Solution**:
```bash
# Auto-fix most issues
ruff check . --fix

# Format code
ruff format .
```

### MCP Connection Issues

**Problem**: Can't connect to Strava MCP server

**Solution**:
- Verify Node.js installed: `node --version`
- Check `mcp_config.json` syntax
- Verify credentials in `mcp_config.json`
- Check server is running: `lsof -i :3000` (Unix) or `netstat -ano | findstr :3000` (Windows)

## Performance Tips

### Async Best Practices

```python
# Good: Concurrent requests
async def fetch_multiple(ids: list[str]) -> list[Workout]:
    tasks = [fetch_workout(id) for id in ids]
    return await asyncio.gather(*tasks)

# Bad: Sequential requests
async def fetch_multiple(ids: list[str]) -> list[Workout]:
    results = []
    for id in ids:
        results.append(await fetch_workout(id))
    return results
```

### Caching

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_calculation(x: int) -> int:
    # Cached for repeated calls
    return x * x
```

## Resources

- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [pytest Documentation](https://docs.pytest.org/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Google ADK](https://google.github.io/adk-docs/)
- [MCP Specification](https://modelcontextprotocol.io/)

## Related Documentation

- [Contributing Guide](../CONTRIBUTING.md)
- [Architecture Overview](architecture.md)
- [Testing Guide](testing.md)
- [MCP Integration](mcp-integration.md)
