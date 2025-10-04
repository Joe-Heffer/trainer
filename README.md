# trAIner

An open-source agentic AI personal trainer for fitness and health that's powered by Strava data.

## Features

- **AI-Powered Coaching**: Leverages large language models (LLMs) through ADK for intelligent training advice
- **Strava Integration**: Connects to your Strava data via MCP (Model Context Protocol)
- **Workout Analysis**: Get detailed feedback on your activities with personalized recommendations
- **Training Plans**: Generate customized training plans based on your goals and fitness level
- **Conversational Interface**: Chat with your AI trainer about training, recovery, and performance

## Prerequisites

- Python 3.13+
- Google Gemini API key ([get one here](https://aistudio.google.com/app/apikey))
- Strava account and API credentials ([register an app](https://www.strava.com/settings/api))

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/trainer.git
   cd trainer
   ```

2. Install the package:
   ```bash
   pip install -e .
   ```

3. Install development dependencies (optional):
   ```bash
   pip install -e ".[dev]"
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

5. Configure the Strava MCP server:
   - Update `mcp_config.json` with your Strava credentials
   - Start the MCP server (see [MCP documentation](https://modelcontextprotocol.io/))

## Quick Start

Run the interactive CLI:

```bash
# After installation
trainer

# Or without installation
python -m trainer
```

For programmatic usage, see the `examples/` directory:

```python
from trainer.agents.trainer_agent import TrainerAgent

# Initialize the trainer
agent = TrainerAgent()
await agent.initialize()

# Analyze a workout
analysis = await agent.analyze_workout("your_activity_id")

# Create a training plan
plan = await agent.create_training_plan(
    goal="Run a half marathon under 2 hours",
    weeks=12
)
```

## Project Structure

```
trainer/
├── src/trainer/
│   ├── agents/          # AI agent implementations
│   ├── models/          # Data models (Pydantic)
│   ├── tools/           # MCP integrations (Strava)
│   └── utils/           # Utilities and helpers
├── tests/
│   ├── unit/            # Unit tests
│   └── integration/     # Integration tests
├── examples/            # Example scripts
└── pyproject.toml       # Project configuration
```

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed development guidelines.

Quick commands:
```bash
# Run tests
pytest

# Lint and format
ruff check . && ruff format .

# Type checking
mypy src/trainer
```

## Documentation

- [Installation Guide](docs/installation.md)
- [Architecture Overview](docs/architecture.md)
- [MCP Integration](docs/mcp-integration.md)
- [Testing Guide](docs/testing.md)
