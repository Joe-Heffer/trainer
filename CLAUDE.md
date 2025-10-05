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

# Set up Strava MCP Server
git clone https://github.com/r-huijts/strava-mcp.git
cd strava-mcp
npm install
npm run build
npx tsx scripts/setup-auth.ts  # Follow prompts to authenticate with Strava

# Set up environment
cp .env.example .env
# Edit .env to add:
# - GEMINI_API_KEY: Your Google Gemini API key
# - STRAVA_MCP_PATH: Absolute path to strava-mcp/dist/server.js
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
   - `strava_mcp.py`: MCP-based Strava integration using r-huijts/strava-mcp
   - Provides functions: `get_athlete_profile()`, `get_athlete_stats()`, `get_recent_activities()`, `get_activity_details()`, `list_athlete_clubs()`, `get_segment()`

4. **Utils** (`src/trainer/utils/`)
   - `config.py`: Environment and configuration management
   - `formatters.py`: Format durations, distances, and paces for display

### MCP Integration

The project uses the **r-huijts/strava-mcp** server for accessing Strava data via the Model Context Protocol (MCP).

**Setup:**
1. Clone and build the strava-mcp server (see Development Setup above)
2. Authenticate with Strava using `npx tsx scripts/setup-auth.ts`
3. Configure `STRAVA_MCP_PATH` in `.env` to point to the server's `dist/server.js` file
4. The MCP client automatically launches the server via stdio communication when tools are called

**Available Tools:**
- `get_athlete_profile()`: Get authenticated athlete's profile
- `get_athlete_stats()`: Get recent, YTD, and all-time statistics
- `get_recent_activities(per_page)`: Fetch recent activities
- `get_activity_details(activity_id)`: Get detailed activity data
- `list_athlete_clubs()`: List athlete's clubs
- `get_segment(segment_id)`: Get segment details

The server is spawned on-demand when the agent uses Strava tools.

### Data Flow

1. User interacts with TrainerAgent
2. Agent calls Strava MCP tools (e.g., `get_athlete_stats()`, `get_recent_activities()`)
3. MCP client spawns the strava-mcp server via stdio and calls the appropriate tool
4. Strava MCP server fetches data from Strava API using stored tokens
5. Data is returned to the agent
6. Agent processes data with Gemini (via Google ADK)
7. Returns structured analysis/recommendations to user
