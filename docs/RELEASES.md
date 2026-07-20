# EmemediaForge — Releases & Installation Guide

No PyPI. Distribution is via GitHub Releases only.
GitHub Actions builds and publishes everything automatically on `git tag` push.

---

## Installing EmemediaForge

### Option 1 — git clone (recommended)

```bash
git clone https://github.com/Ememzyvisuals/ememediaforge.git
cd ememediaforge
pip install .
forge version
```

For development (editable install — changes reflect immediately):
```bash
pip install -e ".[dev]"
```

### Option 2 — pip direct from a GitHub Release

No git required. Go to the [Releases page](https://github.com/Ememzyvisuals/ememediaforge/releases),
copy the `.whl` URL, then:

```bash
pip install https://github.com/Ememzyvisuals/ememediaforge/releases/download/v1.0.0/ememediaforge-1.0.0-py3-none-any.whl
```

### Option 3 — pip from git (always latest main)

```bash
pip install git+https://github.com/Ememzyvisuals/ememediaforge.git
```

Pin to a specific tag:
```bash
pip install git+https://github.com/Ememzyvisuals/ememediaforge.git@v1.0.1
```

### Option 4 — Kaggle / Colab

```python
!apt install ffmpeg -y -q
!pip install git+https://github.com/Ememzyvisuals/ememediaforge.git -q
```

---

## Releasing a New Version (You)

Everything is automated. Three commands:

```bash
# 1. Commit your changes
git add .
git commit -m "feat: add Igbo language support"

# 2. Push code
git push origin main --force

# 3. Tag the release — this triggers everything
git tag v1.0.1
git push origin v1.0.1 --force
```

GitHub Actions then:
- Runs all 22 tests (blocks if any fail)
- Builds `.whl` + `.tar.gz`
- Creates the GitHub Release with auto-changelog
- Attaches the wheel so users can `pip install` from the URL

Done. Takes ~4 minutes.

---

## Versioning

Follows [Semantic Versioning](https://semver.org/):

| Change type | Example | Tag |
|-------------|---------|-----|
| Bug fix | Fix waveform crash on short audio | `v1.0.1` |
| New feature | Add `ocean` theme | `v1.1.0` |
| Breaking change | New YAML config format | `v2.0.0` |
| Beta / testing | New template preview | `v1.1.0-beta.1` |

Pre-release tags (`-beta`, `-rc`, `-alpha`) are marked as pre-release
on GitHub and **won't** show as the latest version to users. Safe to ship.

---

## Make Commands

```bash
make install      # pip install -e ".[dev]"
make test         # pytest
make test-cov     # pytest + coverage report
make lint         # ruff check
make release v=1.0.1        # commit + tag + push in one command
make release-beta v=1.1.0-beta.1
```
