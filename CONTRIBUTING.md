# Contributing to EmemediaForge

Thank you for contributing to EmemediaForge!

## Setup

```bash
git clone https://github.com/Ememzyvisuals/ememediaforge.git
cd ememediaforge
pip install -e ".[dev]"
```

## Code Style

- **Formatter**: ruff (`ruff format .`)
- **Linter**: ruff (`ruff check .`)
- **Type checker**: mypy
- **Line length**: 100 characters

## Testing

```bash
pytest tests/ -v
pytest tests/ --cov=ememediaforge
```

## Pull Request Guidelines

1. Open an issue first for large changes
2. All tests must pass
3. Add tests for new features
4. Update README if user-facing behavior changes
5. Follow existing code style

## Project Structure

See README.md → File Structure section.

## Areas for Contribution

- Additional themes (e.g. `ocean`, `sunset`)
- Additional templates (e.g. `comparison`, `evaluation`)
- Better word alignment algorithms
- Performance improvements
- Platform-specific testing (macOS/Windows)
- Documentation improvements
