# Installation Guide

## Prerequisites

Before installing trAIner, ensure you have:

- **Python 3.13 or higher** - [Download Python](https://www.python.org/downloads/)
- **pip** - Usually included with Python
- **Git** - [Download Git](https://git-scm.com/downloads)
- **Google Gemini API key** - [Get your key](https://aistudio.google.com/app/apikey)
- **Strava account** - [Sign up](https://www.strava.com/register)

## Installation Methods

### Method 1: Install from Source (Recommended for Development)

```bash
# Clone the repository
git clone https://github.com/yourusername/trainer.git
cd trainer

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode
pip install -e .

# For development with testing tools
pip install -e ".[dev]"
```

### Method 2: Install from PyPI (Coming Soon)

```bash
pip install trainer
```

## Configuration

### 1. Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```env
# Google Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# Strava MCP Server URL
STRAVA_MCP_URL=http://localhost:3000
```

### 2. Strava API Setup

1. **Register a Strava Application:**
   - Go to [Strava API Settings](https://www.strava.com/settings/api)
   - Create a new application
   - Note your **Client ID** and **Client Secret**

2. **Configure Authorization:**
   - Set Authorization Callback Domain (e.g., `localhost`)
   - Generate access token with required scopes:
     - `activity:read`
     - `activity:read_all`
     - `profile:read_all`

### 3. MCP Server Setup

The Strava MCP server runs separately from trAIner. Configure it in `mcp_config.json`:

```json
{
  "strava": {
    "url": "http://localhost:3000",
    "credentials": {
      "client_id": "your_client_id",
      "client_secret": "your_client_secret",
      "access_token": "your_access_token"
    }
  }
}
```

See [MCP Integration Guide](mcp-integration.md) for detailed setup instructions.

## Verification

Test your installation:

```bash
# Run the CLI
trainer

# Or run as a module
python -m trainer

# Run tests (if dev dependencies installed)
pytest
```

You should see:
```
🏃 trAIner - Your AI Personal Trainer
========================================

Agent initialized. Type 'quit' or 'exit' to stop.

You:
```

## Troubleshooting

### Python Version Issues

```bash
# Check your Python version
python --version

# If you have multiple versions, use python3.13 explicitly
python3.13 -m venv venv
```

### Missing Dependencies

```bash
# Reinstall dependencies
pip install --upgrade -e ".[dev]"
```

### API Key Errors

- Verify your `.env` file is in the project root
- Check that `GEMINI_API_KEY` is set correctly
- Ensure no extra spaces or quotes around the key

### MCP Connection Issues

- Verify the MCP server is running
- Check the `STRAVA_MCP_URL` in `.env`
- Review [MCP Integration](mcp-integration.md) for setup help

### Import Errors

```bash
# Ensure package is installed
pip list | grep trainer

# Reinstall in editable mode
pip install -e .
```

## Updating

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -e ".[dev]"

# Run tests to verify
pytest
```

## Uninstallation

```bash
pip uninstall trainer
```

## Next Steps

- Read the [Architecture Overview](architecture.md)
- Learn about [MCP Integration](mcp-integration.md)
- Check out example scripts in `examples/`
- Review [CONTRIBUTING.md](../CONTRIBUTING.md) for development
