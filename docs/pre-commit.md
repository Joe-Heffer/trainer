# Pre-commit Hooks Guide

## What is Pre-commit?

Pre-commit is a framework for managing git hooks that automatically run checks before you commit code. This ensures code quality and consistency across all contributions.

## Setup

Pre-commit is included in the dev dependencies:

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Install git hooks
pre-commit install
```

## What Gets Checked

Every time you `git commit`, the following hooks run automatically:

### 1. **Code Quality Checks**
- **trailing-whitespace**: Removes trailing whitespace
- **end-of-file-fixer**: Ensures files end with newline
- **check-merge-conflict**: Detects merge conflict markers
- **debug-statements**: Finds leftover debug statements

### 2. **Format Validation**
- **check-yaml**: Validates YAML syntax
- **check-json**: Validates JSON syntax
- **check-toml**: Validates TOML syntax
- **check-added-large-files**: Prevents committing large files

### 3. **Python Code Quality**
- **ruff**: Lints and auto-fixes code issues
- **ruff-format**: Formats code to style guide
- **mypy**: Type checks Python code

## Usage

### Automatic (Recommended)

Hooks run automatically on every commit:

```bash
git add .
git commit -m "feat: my changes"
# Hooks run automatically here
```

If hooks fail, the commit is blocked until issues are fixed.

### Manual Run

Run hooks manually on all files:

```bash
# Run all hooks
pre-commit run --all-files

# Run specific hook
pre-commit run ruff --all-files
pre-commit run mypy --all-files
```

### Skip Hooks (Not Recommended)

Only skip if absolutely necessary:

```bash
git commit --no-verify -m "emergency fix"
```

## Common Scenarios

### Hooks Modified Your Files

If hooks auto-fix issues:

```bash
$ git commit -m "feat: add feature"
ruff.....................................................................Failed
- files were modified by this hook

# Files were auto-fixed, just add and commit again
git add .
git commit -m "feat: add feature"
```

### Hooks Found Errors

If hooks find issues that can't be auto-fixed:

```bash
$ git commit -m "feat: add feature"
mypy.....................................................................Failed
- exit code: 1
src/trainer/my_file.py:10: error: Incompatible return value type

# Fix the error manually
# Then commit again
git add .
git commit -m "feat: add feature"
```

## Configuration

### Hook Configuration

Hooks are configured in `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

### Updating Hooks

Update to latest hook versions:

```bash
pre-commit autoupdate
```

### Adding New Hooks

Edit `.pre-commit-config.yaml` to add hooks:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: name-tests-test  # Add new hook
```

## Troubleshooting

### Hooks Not Running

**Problem**: Commits succeed without running hooks

**Solution**: Ensure hooks are installed
```bash
pre-commit install
```

### Hook Installation Failed

**Problem**: `pre-commit install` fails

**Solution**: Reinstall pre-commit
```bash
pip install --upgrade --force-reinstall pre-commit
pre-commit install
```

### Mypy Errors

**Problem**: Mypy fails with import errors

**Solution**: Check additional dependencies in `.pre-commit-config.yaml`
```yaml
- id: mypy
  additional_dependencies:
    - pydantic>=2.0.0
```

### Ruff Version Issues

**Problem**: Ruff fails with "unknown variant py313"

**Solution**: Update `target-version` in `pyproject.toml`
```toml
[tool.ruff]
target-version = "py312"  # Use py312 instead of py313
```

## Disabling Specific Hooks

### Temporarily Skip a Hook

```bash
SKIP=mypy git commit -m "WIP: work in progress"
```

### Disable a Hook Permanently

Remove or comment out in `.pre-commit-config.yaml`:

```yaml
  # - repo: https://github.com/pre-commit/mirrors-mypy
  #   rev: v1.8.0
  #   hooks:
  #     - id: mypy
```

## CI Integration

Pre-commit hooks also run in GitHub Actions (`.github/workflows/ci.yml`), ensuring all PRs meet quality standards even if contributors skip local hooks.

## Best Practices

1. **Always run hooks**: Don't skip unless absolutely necessary
2. **Fix issues immediately**: Address hook failures right away
3. **Update regularly**: Keep hooks up-to-date with `pre-commit autoupdate`
4. **Commit small changes**: Easier to fix hook failures
5. **Run manually before big commits**: `pre-commit run --all-files`

## Related Documentation

- [Developer Guide](developers.md)
- [Testing Guide](testing.md)
- [Contributing Guide](../CONTRIBUTING.md)
