.PHONY: install test test-cov lint format build clean release release-beta

# ── Development ───────────────────────────────────────────────────────────────
install:
	pip install -e ".[dev]"

test:
	pytest tests/ -v --tb=short

test-cov:
	pytest tests/ -v --cov=ememediaforge --cov-report=term-missing --cov-report=html
	@echo "Coverage report: htmlcov/index.html"

lint:
	ruff check ememediaforge/

format:
	ruff format ememediaforge/

clean:
	rm -rf dist/ build/ *.egg-info .pytest_cache htmlcov/ coverage.xml
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null; true
	find . -name "*.pyc" -delete 2>/dev/null; true

# ── Build ─────────────────────────────────────────────────────────────────────
build: clean
	pip install build
	python -m build
	pip install twine
	twine check dist/*
	@echo "Built: $$(ls dist/)"

# ── Release (CI/CD via GitHub Actions — just push a tag) ─────────────────────
# Full stable release → PyPI + GitHub Release
release:
	@if [ -z "$(v)" ]; then echo "Usage: make release v=1.0.1"; exit 1; fi
	@echo "Releasing v$(v)…"
	@sed -i 's/^version = .*/version = "$(v)"/' pyproject.toml
	@git add pyproject.toml CHANGELOG.md
	@git commit -m "chore: bump version to v$(v)"
	@git tag v$(v)
	@git push origin main
	@git push origin v$(v)
	@echo "✓ Tag v$(v) pushed — GitHub Actions will publish to PyPI automatically"
	@echo "  Watch: https://github.com/Ememzyvisuals/ememediaforge/actions"

# Pre-release (beta) → TestPyPI only
release-beta:
	@if [ -z "$(v)" ]; then echo "Usage: make release-beta v=1.1.0-beta.1"; exit 1; fi
	@git tag v$(v)
	@git push origin v$(v)
	@echo "✓ Beta tag v$(v) pushed → TestPyPI only"

# ── Demo ──────────────────────────────────────────────────────────────────────
demo:
	forge build example/project.yaml --output example/dist
