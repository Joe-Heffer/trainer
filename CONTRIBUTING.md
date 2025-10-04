# Contributing to trAIner

Thank you for your interest in contributing to trAIner! This guide will help you get started.

## Development Setup

This tool is built with [Google Agent Development Kit](https://google.github.io/adk-docs/) (ADK).

### Prerequisites

- Python
- Git
- A Google Gemini API key
- Strava account and API credentials

### Installation

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/yourusername/trainer.git
   cd trainer
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

## Development Workflow

### Code Style

We use `ruff` for linting and formatting, and `mypy` for type checking.

**Before committing:**

```bash
# Format code
ruff format .

# Check for issues
ruff check .

# Type check
mypy src/trainer
```

**Configuration:**
- Line length: 100 characters
- Target: Python 3.13
- Style: See `pyproject.toml` for full ruff configuration

### Testing

We use `pytest` with async support.

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=trainer --cov-report=html

# Run specific test types
pytest tests/unit
pytest tests/integration

# Run specific test file
pytest tests/unit/test_formatters.py -v
```

**Writing Tests:**
- Place unit tests in `tests/unit/`
- Place integration tests in `tests/integration/`
- Use descriptive test names: `test_<function>_<scenario>_<expected_result>`
- Use fixtures for common setup
- Mock external services (Strava MCP, Gemini API)

### Project Structure

```
src/trainer/
├── agents/           # AI agent implementations
│   └── trainer_agent.py
├── models/           # Pydantic data models
├── tools/            # MCP client integrations
├── utils/            # Helper functions
│   ├── config.py     # Configuration management
│   └── formatters.py # Display formatters
└── __main__.py       # CLI entry point
```

### Making Changes

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes:**
   - Write code following the style guide
   - Add tests for new functionality
   - Update documentation as needed

3. **Run quality checks:**
   ```bash
   ruff format .
   ruff check .
   mypy src/trainer
   pytest
   ```

4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

   **Commit message format:**
   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation changes
   - `test:` - Test additions/changes
   - `refactor:` - Code refactoring
   - `chore:` - Maintenance tasks

5. **Push and create a pull request:**
   ```bash
   git push origin feature/your-feature-name
   ```

## Areas for Contribution

### High Priority
- Complete TrainerAgent implementation
- Strava MCP integration
- Workout analysis logic
- Training plan generation
- Error handling and validation

### Documentation
- Usage examples
- API documentation
- Tutorial guides
- Architecture diagrams

### Testing
- Increase test coverage
- Add integration tests
- Add edge case tests

### Features
- Additional sports support
- Advanced analytics
- Visualization tools
- Export functionality

## Code Review Process

1. Ensure all tests pass
2. Ensure code quality checks pass
3. Update relevant documentation
4. Submit PR with clear description
5. Address reviewer feedback
6. Squash commits if requested

## Questions?

- Open an issue for bugs or feature requests
- Start a discussion for questions or ideas
- Check existing issues before creating new ones

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
