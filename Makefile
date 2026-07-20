.PHONY: install test test-cov lint format clean release release-beta demo

install:
	pip install -e ".[dev]"

test:
	pytest tests/ -v --tb=short

test-cov:
	pytest tests/ -v --cov=ememediaforge --cov-report=term-missing

lint:
	ruff check ememediaforge/

format:
	ruff format ememediaforge/

clean:
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null; true
	find . -name "*.pyc" -delete 2>/dev/null; true
	rm -rf dist/ build/ *.egg-info .pytest_cache htmlcov/ coverage.xml

# ── Release — just tag and push, GitHub Actions handles the rest ──────────────
release:
	@if [ -z "$(v)" ]; then \
		echo "Usage: make release v=1.0.1"; exit 1; \
	fi
	@echo "Releasing v$(v)..."
	@sed -i 's/^version = .*/version = "$(v)"/' pyproject.toml
	@git add pyproject.toml
	@git commit -m "chore: bump version to v$(v)"
	@git tag v$(v)
	@git push origin main --force
	@git push origin v$(v) --force
	@echo ""
	@echo "✓ Tag v$(v) pushed."
	@echo "  GitHub Actions is now running:"
	@echo "  → tests → build → GitHub Release"
	@echo ""
	@echo "  Watch: https://github.com/Ememzyvisuals/ememediaforge/actions"
	@echo "  Release: https://github.com/Ememzyvisuals/ememediaforge/releases"

release-beta:
	@if [ -z "$(v)" ]; then \
		echo "Usage: make release-beta v=1.1.0-beta.1"; exit 1; \
	fi
	@git tag v$(v)
	@git push origin v$(v) --force
	@echo "✓ Beta tag v$(v) pushed → GitHub pre-release"

demo:
	forge build example/project.yaml --output example/dist
