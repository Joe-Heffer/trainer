[![Continuous integration](https://github.com/Joe-Heffer/trainer/actions/workflows/ci.yml/badge.svg)](https://github.com/Joe-Heffer/trainer/actions/workflows/ci.yml)
[![Dependabot Updates](https://github.com/Joe-Heffer/trainer/actions/workflows/dependabot/dependabot-updates/badge.svg)](https://github.com/Joe-Heffer/trainer/actions/workflows/dependabot/dependabot-updates)

# trAIner

An open-source agentic AI personal trainer for fitness and health that's powered by Strava data.

![Personal trainer](images/athena.jpg)

## Features

- **AI-Powered Coaching**: Get intelligent training advice powered by advanced LLMs
- **Strava Integration**: Automatically analyze your workouts from Strava
- **Workout Analysis**: Receive detailed feedback with personalized recommendations
- **Training Plans**: Generate customized plans based on your goals and fitness level
- **Conversational Interface**: Chat naturally with your AI trainer about training, recovery, and performance

## Quick Start

### Prerequisites

- Python 3.13+
- Google Gemini API key ([get one here](https://aistudio.google.com/app/apikey))
- Strava account ([sign up](https://www.strava.com/register))

### Installation

1. **Clone and install:**

   ```bash
   git clone https://github.com/Joe-Heffer/trainer.git
   cd trainer
   pip install -e .
   ```

2. **Set up Strava MCP Server:**

   ```bash
   # Clone and build the Strava MCP server
   git clone https://github.com/r-huijts/strava-mcp.git
   cd strava-mcp
   npm install
   npm run build

   # Authenticate with Strava (creates API app and gets tokens)
   npx tsx scripts/setup-auth.ts
   # Follow the prompts to authorize with Strava
   ```

3. **Configure environment:**

   ```bash
   cd ../trainer
   cp .env.example .env
   # Edit .env and add:
   # - GEMINI_API_KEY: Your Google Gemini API key (https://aistudio.google.com/apikey)
   # - STRAVA_MCP_PATH: Absolute path to strava-mcp/dist/server.js
   ```

## Usage

### Command line

```bash
trainer
```

For the arguments:

```bash
trainer --help
```

### Programmatic

```python
from trainer import TrainerAgent

agent = TrainerAgent()
await agent.initialize()

# Analyze a workout
analysis = await agent.analyze_workout("activity_id")

# Create a training plan
plan = await agent.create_training_plan(
    goal="Run a half marathon under 2 hours",
    weeks=12
)
```

## Example Conversation

```
You: How was my last run?

Trainer: Your 10K run this morning was solid! You maintained a consistent
pace of 5:30/km with good heart rate control in zone 2. Your cadence of
178 spm is excellent. Consider adding some hills next time to build strength.

You: Create a 12-week plan to run a marathon

Trainer: I'll create a progressive 12-week marathon plan building from your
current fitness level...
```

## Documentation

**For Users:**

- [Installation Guide](docs/installation.md) - Detailed setup instructions
- [MCP Integration](docs/mcp-integration.md) - Connecting to Strava

**For Contributors:**

- [Contributing Guide](CONTRIBUTING.md) - How to contribute
- [Developer Guide](docs/developers.md) - Development setup and workflows
- [Architecture](docs/architecture.md) - System design and components
- [Testing Guide](docs/testing.md) - Writing and running tests

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) to get started.

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/trainer/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/trainer/discussions)

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

Built with:

- [Google Agent Development Kit (ADK)](https://google.github.io/adk-docs/)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [r-huijts/strava-mcp](https://github.com/r-huijts/strava-mcp) - Strava MCP server
- [Strava API](https://developers.strava.com/)
