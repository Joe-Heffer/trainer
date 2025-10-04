# Examples

This directory contains example scripts demonstrating how to use trAIner.

## Prerequisites

1. Install dependencies:
   ```bash
   pip install -e .
   ```

2. Set up your environment variables (copy `.env.example` to `.env`):
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `STRAVA_MCP_URL`: URL of your Strava MCP server

3. Configure and start the Strava MCP server (see `mcp_config.json`)

## Examples

### basic_usage.py
Demonstrates basic trainer agent functionality including:
- Initializing the agent
- Analyzing workouts
- Chatting with the AI trainer
- Creating training plans

Run with:
```bash
python examples/basic_usage.py
```

### strava_integration.py
Shows how to interact with Strava data through the MCP client:
- Fetching athlete statistics
- Retrieving recent activities
- Getting detailed activity information

Run with:
```bash
python examples/strava_integration.py
```
