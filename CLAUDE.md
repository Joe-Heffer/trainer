# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

trAIner is an open-source agentic AI personal trainer for fitness and health, built with Google ADK (Gemini) and powered by Strava data through MCP (Model Context Protocol).

## Technology Stack

- **Language**: Python 3.13+
- **AI Framework**: Google ADK (google-genai)
- **Integration**: Strava MCP Server
- **Data Validation**: Pydantic v2
- **Testing**: pytest with async support
- **Code Quality**: ruff (linter/formatter), mypy (type checking)
- **Build System**: Hatchling

## Commands

### Development Setup
```bash
# Install package in editable mode
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"

# Set up environment
cp .env.example .env
# Edit .env to add GEMINI_API_KEY and STRAVA_MCP_URL
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=trainer --cov-report=html

# Run only unit tests
pytest tests/unit

# Run only integration tests
pytest tests/integration

# Run specific test file
pytest tests/unit/test_formatters.py
```

### Code Quality
```bash
# Lint and check code
ruff check .

# Format code
ruff format .

# Type checking
mypy src/trainer
```

## Architecture

### Core Components

1. **Agents** (`src/trainer/agents/`)
   - `TrainerAgent`: Main agentic AI trainer using Google ADK
   - Handles workout analysis, training plan generation, and conversational coaching
   - Integrates with Strava MCP tool for activity data

2. **Models** (`src/trainer/models/`)
   - `Workout`: Represents Strava activity data
   - `WorkoutAnalysis`: Structured analysis output with recommendations
   - `TrainingPlan`: Multi-week training plan structure
   - All models use Pydantic for validation

3. **Tools** (`src/trainer/tools/`)
   - `StravaClient`: MCP client for Strava integration
   - Provides methods to fetch athlete stats, activities, and detailed workout data

4. **Utils** (`src/trainer/utils/`)
   - `config.py`: Environment and configuration management
   - `formatters.py`: Format durations, distances, and paces for display

### MCP Integration

The project uses the Strava MCP server for accessing Strava data. Configuration is in `mcp_config.json`. The MCP server must be running separately and is accessed via the StravaClient.

### Data Flow

1. User interacts with TrainerAgent
2. Agent may call StravaClient to fetch activity data via MCP
3. Data is validated using Pydantic models
4. Agent processes data with Gemini (via Google ADK)
5. Returns structured analysis/recommendations to user
