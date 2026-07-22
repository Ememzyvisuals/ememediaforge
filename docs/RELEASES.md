# EmemediaForge — Releases & Installation Guide

Distribution is via GitHub Releases only — no PyPI.
GitHub Actions builds and publishes everything automatically on `git tag` push.

---

## Installing EmemediaForge

### Option 1 — git clone (recommended for development)

```bash
git clone https://github.com/Ememzyvisuals/ememediaforge.git
cd ememediaforge
pip install .
forge version
```

Editable install (changes to source reflect immediately):
```bash
pip install -e ".[dev]"
```

### Option 2 — pip direct from latest GitHub Release

No git required. Always installs the latest stable version:

```bash
pip install https://github.com/Ememzyvisuals/ememediaforge/releases/latest/download/ememediaforge-py3-none-any.whl
```

Or pin to a specific version:
```bash
pip install https://github.com/Ememzyvisuals/ememediaforge/releases/download/v1.0.3/ememediaforge-1.0.3-py3-none-any.whl
```

### Option 3 — pip from git tag

```bash
# Latest main branch
pip install git+https://github.com/Ememzyvisuals/ememediaforge.git

# Specific version tag
pip install git+https://github.com/Ememzyvisuals/ememediaforge.git@v1.0.3
```

### Option 4 — Kaggle / Colab

```python
!apt install ffmpeg -y -q
!pip install git+https://github.com/Ememzyvisuals/ememediaforge.git -q
!forge build project.yaml --fast   # always use --fast on shared CPU
```

---

## Releasing a New Version

Three commands — GitHub Actions handles everything else:

```bash
# 1. Commit changes
git add .
git commit -m "feat: your change here"

# 2. Push
git push origin main --force

# 3. Tag — triggers the full release pipeline
git tag v1.0.4
git push origin v1.0.4 --force
```

Or with the Makefile shortcut:
```bash
make release v=1.0.4
```

**What GitHub Actions does:**
1. Runs 22 tests across Python 3.10 / 3.11 / 3.12 (blocks if any fail)
2. Builds `.whl` + `.tar.gz`, version synced from the tag
3. Generates a NaijaVox 2.0 demo video using `forge build --fast`
4. Creates a GitHub Release with:
   - Auto-generated changelog from conventional commits
   - `.whl` and `.tar.gz` attached
   - `demo.mp4`, `thumbnail.png`, `metadata.json` attached

Total time: ~5–7 minutes from tag push to live release.

---

## Pre-releases (beta, RC)

```bash
git tag v1.1.0-beta.1
git push origin v1.1.0-beta.1 --force
```

Tags containing `-` are automatically marked as **pre-release** on GitHub and
won't show as the latest version to users installing from releases.

---

## Version history

| Version | Date | Highlights |
|---------|------|------------|
| v1.0.3 | 2026-07-22 | Fix `--fast` not registered in Typer CLI signature |
| v1.0.2 | 2026-07-22 | Add `--fast` flag; fix FFmpeg stderr deadlock (6h CI hang) |
| v1.0.1 | 2026-07-21 | Fix 80 ruff errors; CI now passes lint step |
| v1.0.0 | 2026-07-20 | Initial release |

Full details: [CHANGELOG.md](../CHANGELOG.md)

---

## Make commands

```bash
make install           # pip install -e ".[dev]"
make test              # pytest
make test-cov          # pytest + coverage report
make lint              # ruff check
make format            # ruff format
make release v=1.0.4   # bump version + commit + tag + push
make release-beta v=1.1.0-beta.1
```
