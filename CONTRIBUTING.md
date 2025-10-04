# Contributing to trAIner

Thank you for your interest in contributing! Whether you're fixing bugs, adding features, or improving documentation, your help is appreciated.

## Getting Started

### Quick Setup

1. **Fork and clone:**
   ```bash
   git clone https://github.com/yourusername/trainer.git
   cd trainer
   ```

2. **Install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Add your GEMINI_API_KEY for testing
   ```

4. **Verify setup:**
   ```bash
   pytest
   ```

For detailed development setup, see [Developer Guide](docs/developers.md).

## How to Contribute

### Reporting Issues

- **Bug reports**: Include steps to reproduce, expected vs actual behavior
- **Feature requests**: Describe the use case and proposed solution
- **Questions**: Use GitHub Discussions for general questions

### Code Contributions

1. **Find or create an issue** to discuss your changes
2. **Create a feature branch:**
   ```bash
   git checkout -b feat/your-feature
   ```
3. **Make your changes** (see [Developer Guide](docs/developers.md))
4. **Test your changes:**
   ```bash
   pytest
   ruff format . && ruff check .
   mypy src/trainer
   ```
5. **Commit using conventional commits:**
   ```bash
   git commit -m "feat: add workout comparison feature"
   ```
6. **Push and open a pull request**

### Commit Message Format

Use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation only
- `test:` - Adding/updating tests
- `refactor:` - Code refactoring
- `chore:` - Maintenance tasks
- `ci:` - CI/CD changes

Examples:
```
feat: add support for cycling workouts
fix: correct pace calculation for intervals
docs: update installation guide
test: add tests for training plan generation
```

## Pull Request Guidelines

### Before Submitting

- ✅ All tests pass (`pytest`)
- ✅ Code is formatted (`ruff format .`)
- ✅ No linting errors (`ruff check .`)
- ✅ Type checking passes (`mypy src/trainer`)
- ✅ Documentation is updated if needed
- ✅ Tests added for new features

### PR Description

Include:
- **What**: Brief description of changes
- **Why**: Motivation and context
- **How**: Implementation approach (if complex)
- **Testing**: How you tested the changes
- **Screenshots**: For UI changes

### Review Process

1. Automated checks run (CI/CD)
2. Maintainer reviews code
3. Address feedback if needed
4. Approved PRs are merged

## What to Contribute

### 🔥 High Priority

- Complete TrainerAgent implementation
- Strava MCP integration
- Workout analysis features
- Training plan generation
- Error handling improvements

### 📚 Documentation

- Usage examples
- Tutorial guides
- API documentation
- Video walkthroughs

### 🧪 Testing

- Increase test coverage
- Integration tests
- Edge case testing
- Performance testing

### ✨ Features

Looking for ideas? Check out:
- [Good First Issues](https://github.com/yourusername/trainer/labels/good%20first%20issue)
- [Feature Requests](https://github.com/yourusername/trainer/labels/enhancement)
- [Help Wanted](https://github.com/yourusername/trainer/labels/help%20wanted)

## Code Style

We follow these conventions:

- **Python**: PEP 8 via ruff (100 char line length)
- **Type hints**: Required for all functions
- **Docstrings**: Google style for public APIs
- **Async**: Use async/await for I/O operations
- **Imports**: Sorted with ruff

Example:
```python
async def analyze_workout(workout_id: str) -> WorkoutAnalysis:
    """Analyze a workout and provide feedback.

    Args:
        workout_id: Strava activity ID

    Returns:
        Detailed workout analysis with recommendations
    """
    # Implementation
```

## Testing Requirements

- **Unit tests** for all new functions
- **Integration tests** for API interactions
- **Mocks** for external services (Gemini, Strava)
- **Coverage**: Aim for >80% overall

See [Testing Guide](docs/testing.md) for details.

## Community Guidelines

- Be respectful and inclusive
- Provide constructive feedback
- Help newcomers
- Stay on topic in discussions
- Follow the [Code of Conduct](CODE_OF_CONDUCT.md)

## Development Resources

- [Developer Guide](docs/developers.md) - Detailed development workflows
- [Architecture Overview](docs/architecture.md) - System design
- [Testing Guide](docs/testing.md) - Testing best practices
- [MCP Integration](docs/mcp-integration.md) - Strava connection

## Recognition

Contributors are recognized in:
- GitHub contributors page
- Release notes
- Project acknowledgments

## Questions?

- **General questions**: [GitHub Discussions](https://github.com/yourusername/trainer/discussions)
- **Bug reports**: [GitHub Issues](https://github.com/yourusername/trainer/issues)
- **Security**: Email security@yourproject.com

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for making trAIner better! 🏃‍♂️
