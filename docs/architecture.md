# Architecture Overview

## System Design

trAIner is built as a modular, agentic AI system that combines Google's Gemini models with real-time fitness data from Strava to provide personalized training guidance.

```
┌─────────────┐
│    User     │
└──────┬──────┘
       │
       v
┌─────────────────────────────────────┐
│         CLI / Interface             │
│         (__main__.py)               │
└──────────────┬──────────────────────┘
               │
               v
┌─────────────────────────────────────┐
│       TrainerAgent                  │
│   (Google ADK / Gemini)             │
│                                     │
│  - Workout Analysis                 │
│  - Training Plan Generation         │
│  - Conversational Coaching          │
└──────────┬──────────────────────────┘
           │
           v
┌──────────────────────┐
│   StravaClient       │
│   (MCP Integration)  │
└──────────┬───────────┘
           │
           v
┌──────────────────────┐
│   Strava MCP Server  │
│   (External Service) │
└──────────────────────┘
```

## Core Components

### 1. Agents (`src/trainer/agents/`)

**TrainerAgent** (`trainer_agent.py`)
- Primary AI agent using Google ADK (Agentic Development Kit)
- Powered by Gemini 2.0 Flash Exp model by default
- Capabilities:
  - Analyze workouts with personalized feedback
  - Generate multi-week training plans
  - Provide conversational coaching
  - Integrate with Strava data via MCP tools

**Key Methods:**
- `initialize()` - Set up agent with tools and instructions
- `process_message(message)` - Handle conversational interactions
- `analyze_workout(workout_id)` - Deep analysis of specific activities
- `create_training_plan(goal, weeks)` - Generate structured training plans

### 2. Models (`src/trainer/models/`)

Data models built with Pydantic v2 for validation and serialization.

**Workout** (`workout.py`)
- Represents Strava activity data
- Fields: id, name, type, distance, duration, heart rate, speed, calories
- Validated types ensure data integrity

**WorkoutAnalysis** (`workout.py`)
- Structured output from workout analysis
- Fields: summary, strengths, improvements, recommendations, effort rating
- Ensures consistent AI responses

**TrainingPlan** (`training_plan.py`)
- Multi-week training plan structure
- Defines weekly workouts, goals, and progression
- Supports various training goals (distance, speed, endurance)

### 3. Tools (`src/trainer/tools/`)

**StravaClient** (`strava_client.py`)
- MCP (Model Context Protocol) integration for Strava
- Provides methods to fetch:
  - Athlete statistics
  - Recent activities
  - Detailed workout data
- Async API for non-blocking operations

**Integration Pattern:**
```python
client = StravaClient(mcp_server_url)
activities = await client.get_recent_activities(limit=30)
details = await client.get_activity_details(activity_id)
```

### 4. Utils (`src/trainer/utils/`)

**config.py**
- Environment variable management
- Configuration loading from `.env`
- Centralized settings (API keys, URLs, defaults)

**formatters.py**
- Human-readable formatting utilities
- Duration formatting (seconds → "1h 23m 45s")
- Distance formatting (meters → "5.2 km" / "3.2 mi")
- Pace calculations (min/km, min/mi)

### 5. CLI Entry Point (`__main__.py`)

- Interactive command-line interface
- Manages conversation loop with TrainerAgent
- Handles user input/output
- Graceful error handling and shutdown

## Data Flow

### Workout Analysis Flow

```
User Request
    ↓
TrainerAgent.analyze_workout(id)
    ↓
StravaClient.get_activity_details(id)
    ↓
MCP Server → Strava API
    ↓
Raw Activity Data
    ↓
Workout Model (Pydantic validation)
    ↓
Gemini Analysis (via ADK)
    ↓
WorkoutAnalysis Model
    ↓
Return to User
```

### Training Plan Generation Flow

```
User Goal + Duration
    ↓
TrainerAgent.create_training_plan(goal, weeks)
    ↓
StravaClient.get_athlete_stats()
    ↓
Current Fitness Assessment
    ↓
Gemini Plan Generation (via ADK)
    ↓
TrainingPlan Model
    ↓
Return to User
```

## Technology Stack

### AI Framework
- **Google ADK (google-genai)**: Agentic AI development kit
- **Gemini 2.0 Flash Exp**: Default model for fast, intelligent responses
- Supports tool calling for Strava integration

### Data Integration
- **MCP (Model Context Protocol)**: Standard for AI-tool integration
- **Strava API**: Fitness data source via MCP server
- **Async/await**: Non-blocking I/O for API calls

### Data Validation
- **Pydantic v2**: Runtime type checking and validation
- Ensures data integrity throughout the pipeline
- Automatic serialization/deserialization

### Development Tools
- **pytest**: Testing framework with async support
- **ruff**: Fast Python linter and formatter
- **mypy**: Static type checking
- **hatchling**: Modern Python build backend

## Design Principles

### 1. Modularity
- Clear separation of concerns (agents, models, tools, utils)
- Easy to extend with new agents or data sources
- Components can be tested independently

### 2. Type Safety
- Python 3.13+ with modern type hints
- Pydantic models for runtime validation
- mypy for static analysis

### 3. Async-First
- All I/O operations use async/await
- Non-blocking API calls to Strava and Gemini
- Better performance for concurrent operations

### 4. Testability
- Dependency injection for external services
- Mock-friendly architecture
- Comprehensive test coverage

### 5. Extensibility
- Plugin-style architecture for new tools
- Easy to add new workout types or analysis features
- MCP allows integration with any MCP-compatible service

## Future Architecture Considerations

### Planned Enhancements
1. **Multi-Agent System**: Specialized agents for different sports
2. **Caching Layer**: Store frequently accessed Strava data
3. **Database Integration**: Persist user preferences and history
4. **Web Interface**: FastAPI backend + React frontend
5. **Real-time Updates**: WebSocket support for live coaching

### Scalability
- Current design supports single-user CLI usage
- Can scale to multi-user with:
  - Database for user data
  - Session management
  - API authentication
  - Rate limiting for external APIs

## Related Documentation

- [Installation Guide](installation.md)
- [MCP Integration](mcp-integration.md)
- [CONTRIBUTING.md](../CONTRIBUTING.md)
