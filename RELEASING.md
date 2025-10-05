# Release Process

This document describes how to publish a new release of trAIner to PyPI.

## Prerequisites

### 1. Configure PyPI Trusted Publishing

Before your first release, set up trusted publishing on PyPI (no API tokens needed):

1. Go to https://pypi.org/manage/account/publishing/
2. Click "Add a new pending publisher"
3. Fill in the form:
   - **PyPI Project Name**: `trainer`
   - **Owner**: Your GitHub username or org (e.g., `Joe-Heffer`)
   - **Repository name**: `trainer`
   - **Workflow name**: `publish.yml`
   - **Environment name**: `pypi`
4. Click "Add"

After the first successful release, the project will be created on PyPI and trusted publishing will be active.

## Release Steps

### 1. Update Version

Edit `pyproject.toml` and update the version number:

```toml
[project]
version = "0.2.0"  # Update this
```

### 2. Update Changelog (if you have one)

Document the changes in `CHANGELOG.md` or release notes.

### 3. Commit and Push

```bash
git add pyproject.toml
git commit -m "chore: bump version to 0.2.0"
git push origin main
```

### 4. Create GitHub Release

```bash
# Create and push a tag
git tag v0.2.0
git push origin v0.2.0

# Or create a release via GitHub UI or CLI
gh release create v0.2.0 --title "v0.2.0" --notes "Release notes here"
```

The GitHub Actions workflow will automatically:
- Build the package
- Publish to PyPI using trusted publishing

### 5. Verify

Check that the package is available:
- PyPI: https://pypi.org/project/trainer/
- Install: `pip install trainer`

## Versioning

This project follows [Semantic Versioning](https://semver.org/):
- **MAJOR** (1.0.0): Breaking changes
- **MINOR** (0.1.0): New features, backwards compatible
- **PATCH** (0.0.1): Bug fixes, backwards compatible

## Troubleshooting

### Trusted Publishing Not Working

- Verify the PyPI trusted publisher configuration matches your repository exactly
- Check that the workflow has `permissions: id-token: write`
- Ensure the workflow runs on `release: published` events

### Build Failures

- Test the build locally: `python -m build`
- Check that all required files are included in the package
- Verify `pyproject.toml` is valid

### Package Name Already Taken

If "trainer" is taken, choose a unique name like "trAIner" or "ai-trainer" and update:
- `pyproject.toml`: `name = "trAIner"`
- PyPI trusted publisher configuration
- This documentation
