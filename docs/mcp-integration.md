# MCP Integration Guide

## What is MCP?

[Model Context Protocol (MCP)](https://modelcontextprotocol.io/) is an open standard that enables AI applications to securely connect to external data sources and tools. trAIner uses MCP to integrate with Strava, allowing the AI trainer to access your workout data.

## Architecture

```
┌─────────────────┐
│  trAIner Agent  │
│  (Google ADK)   │
└────────┬────────┘
         │
         │ MCP Client
         │
         v
┌─────────────────┐
│  StravaClient   │
│  (MCP Bridge)   │
└────────┬────────┘
         │
         │ MCP Protocol
         │
         v
┌─────────────────┐
│ Strava MCP      │
│ Server          │
└────────┬────────┘
         │
         v
┌─────────────────┐
│  Strava API     │
└─────────────────┘
```

## Setup

### Prerequisites

- Node.js 18+ (for running MCP server)
- Strava account
- Strava API application registered

### 1. Register Strava Application

1. Go to [Strava API Settings](https://www.strava.com/settings/api)
2. Click "Create App" or use an existing app
3. Fill in application details:
   - **Application Name**: "trAIner" (or your choice)
   - **Category**: Training
   - **Authorization Callback Domain**: `localhost`
4. Note your **Client ID** and **Client Secret**

### 2. Configure MCP Server

Edit `mcp_config.json` in the project root:

```json
{
  "mcpServers": {
    "strava": {
      "command": "npx",
      "args": ["-y", "@strava/mcp-server"],
      "env": {
        "STRAVA_CLIENT_ID": "your_client_id_here",
        "STRAVA_CLIENT_SECRET": "your_client_secret_here",
        "STRAVA_REDIRECT_URI": "http://localhost:3000/callback"
      }
    }
  }
}
```

### 3. Get Strava Access Token

The Strava MCP server handles OAuth authentication. On first run:

1. Start the MCP server (it will start automatically with trAIner)
2. Navigate to the authorization URL provided
3. Grant permissions to your Strava account
4. The server will receive the access token automatically

**Required Scopes:**
- `activity:read` - Read public activities
- `activity:read_all` - Read private activities
- `profile:read_all` - Read profile information

### 4. Update .env Configuration

Add the MCP server URL to your `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
STRAVA_MCP_URL=http://localhost:3000
```

## Using the Strava MCP Server

### Starting the Server

The MCP server is managed automatically by the MCP protocol implementation. When you run trAIner, it will:

1. Read `mcp_config.json`
2. Start the Strava MCP server via `npx`
3. Establish connection
4. Make tools available to the agent

### Manual Server Management (Optional)

To run the MCP server independently:

```bash
# Install globally
npm install -g @strava/mcp-server

# Run with environment variables
STRAVA_CLIENT_ID=xxx \
STRAVA_CLIENT_SECRET=xxx \
strava-mcp-server
```

## Available MCP Tools

The Strava MCP server provides these tools to the TrainerAgent:

### 1. Get Athlete Profile
```python
# Returns athlete info: name, weight, FTP, heart rate zones
tool: get_athlete
```

### 2. Get Athlete Stats
```python
# Returns stats: recent run distance, ride distance, swim distance
tool: get_athlete_stats
```

### 3. List Recent Activities
```python
# Returns recent activities with basic info
tool: list_activities
params:
  - before: timestamp (optional)
  - after: timestamp (optional)
  - page: int (default: 1)
  - per_page: int (default: 30)
```

### 4. Get Activity Details
```python
# Returns detailed activity data with streams (GPS, HR, power, etc.)
tool: get_activity
params:
  - id: activity_id
```

### 5. Get Activity Streams
```python
# Returns time-series data (heart rate, power, cadence, etc.)
tool: get_activity_streams
params:
  - id: activity_id
  - types: list of stream types
```

## StravaClient Implementation

The `StravaClient` class wraps MCP tool calls:

```python
from trainer.tools.strava_client import StravaClient

# Initialize client
client = StravaClient(mcp_server_url="http://localhost:3000")

# Get recent activities
activities = await client.get_recent_activities(limit=30)

# Get specific activity details
details = await client.get_activity_details(activity_id="12345")

# Get athlete stats
stats = await client.get_athlete_stats()
```

### Data Flow Example

```python
# User asks: "How was my last run?"

# 1. Agent calls StravaClient
activities = await strava_client.get_recent_activities(limit=10)

# 2. Filter for runs
last_run = [a for a in activities if a['type'] == 'Run'][0]

# 3. Get detailed data
details = await strava_client.get_activity_details(last_run['id'])

# 4. Convert to Workout model
workout = Workout(**details)

# 5. Agent analyzes with Gemini
analysis = await agent.analyze_workout(workout)

# 6. Return feedback to user
```

## Troubleshooting

### MCP Server Not Starting

**Error**: "Cannot connect to MCP server"

**Solutions**:
- Ensure Node.js 18+ is installed: `node --version`
- Check `mcp_config.json` syntax is valid JSON
- Verify environment variables are set correctly
- Check firewall isn't blocking localhost:3000

### Authentication Failures

**Error**: "Unauthorized" or "Invalid token"

**Solutions**:
- Re-authenticate with Strava (delete stored tokens)
- Verify Client ID and Secret in `mcp_config.json`
- Check redirect URI matches Strava app settings
- Ensure required scopes are granted

### Missing Activity Data

**Error**: Activities not appearing or incomplete data

**Solutions**:
- Verify Strava privacy settings allow API access
- Check activity visibility (public vs. private)
- Ensure `activity:read_all` scope is granted
- Wait for Strava API sync (can take a few minutes after upload)

### Rate Limiting

**Error**: "Rate limit exceeded"

**Solutions**:
- Strava API limits: 100 requests per 15 minutes, 1000 per day
- Implement caching for frequently accessed data
- Reduce polling frequency
- Use bulk endpoints when possible

## Advanced Configuration

### Custom MCP Server

To use a custom MCP server implementation:

1. Implement MCP protocol specification
2. Update `mcp_config.json` with custom command
3. Ensure tool schemas match expected format

### Multiple Data Sources

MCP supports multiple servers simultaneously:

```json
{
  "mcpServers": {
    "strava": { /* ... */ },
    "garmin": { /* ... */ },
    "whoop": { /* ... */ }
  }
}
```

### Webhook Integration

For real-time activity updates, configure Strava webhooks:

1. Set up webhook endpoint in your MCP server
2. Register webhook with Strava API
3. Process events as they arrive
4. Update local cache/database

## Security Best Practices

1. **Never commit credentials**
   - Add `.env` to `.gitignore`
   - Use environment variables for secrets

2. **Scope minimization**
   - Only request necessary OAuth scopes
   - Review permissions regularly

3. **Token rotation**
   - Refresh tokens before expiration
   - Implement secure token storage

4. **Network security**
   - Use HTTPS for production deployments
   - Validate webhook signatures
   - Implement rate limiting

## Resources

- [MCP Specification](https://modelcontextprotocol.io/specification)
- [Strava API Documentation](https://developers.strava.com/docs/reference/)
- [OAuth 2.0 Guide](https://oauth.net/2/)
- [Google ADK Documentation](https://ai.google.dev/adk)

## Related Documentation

- [Installation Guide](installation.md)
- [Architecture Overview](architecture.md)
- [CONTRIBUTING.md](../CONTRIBUTING.md)
