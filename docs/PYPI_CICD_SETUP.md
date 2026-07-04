# PyPI + GitHub CI/CD — One-Time Setup Guide

Zero-secret, fully automated releases using OIDC Trusted Publisher.
After this setup, releasing is just:  `git tag v1.0.1 && git push origin v1.0.1`

---

## How it works (big picture)

```
git push tag v1.0.0
        │
        ▼
 GitHub Actions: release.yml
        │
        ├─ 1. pytest (must pass)
        ├─ 2. python -m build  →  dist/*.whl + dist/*.tar.gz
        ├─ 3. publish → TestPyPI  (smoke-test install)
        ├─ 4. publish → PyPI      (OIDC — no API token needed ever)
        └─ 5. GitHub Release      (changelog + wheel attached)
```

---

## Step 1 — Create PyPI account

1. Go to → https://pypi.org/account/register/
2. Verify your email
3. Enable 2FA (required for publishing since 2024)

---

## Step 2 — Create TestPyPI account

1. Go to → https://test.pypi.org/account/register/
   (separate account from PyPI — same email is fine)
2. Verify + enable 2FA

---

## Step 3 — Configure OIDC Trusted Publisher on PyPI

This is the magic step — lets GitHub Actions publish WITHOUT API tokens.

### On PyPI (real):
1. Log in → https://pypi.org
2. Click your username → **Publishing**
3. Scroll to **"Add a new pending publisher"**
4. Fill in:
   ```
   PyPI project name:   ememediaforge
   Owner:               Ememzyvisuals
   Repository name:     ememediaforge
   Workflow filename:   release.yml
   Environment name:    pypi
   ```
5. Click **Add**

### On TestPyPI:
1. Log in → https://test.pypi.org
2. Same steps above, but:
   ```
   Environment name:    testpypi
   ```

---

## Step 4 — Create GitHub Environments

In your repo: **Settings → Environments → New environment**

Create two environments:

### `pypi`
- Click **Add deployment protection rules**
- Enable **Required reviewers** (add yourself) — optional but safe
- No secrets needed (OIDC handles auth)

### `testpypi`
- No protection rules needed
- No secrets needed

---

## Step 5 — Push your code

```bash
git init
git remote add origin https://github.com/Ememzyvisuals/ememediaforge.git
git add .
git commit -m "feat: EmemediaForge v1.0.0 — initial release"
git push -u origin main

# Also push develop branch for dev workflow
git checkout -b develop
git push -u origin develop
```

---

## Step 6 — Trigger your first release

```bash
git checkout main

# Bump version in pyproject.toml if needed (CI auto-syncs from tag)
git tag v1.0.0
git push origin v1.0.0
```

Watch it fly at: **github.com/Ememzyvisuals/ememediaforge/actions**

Pipeline takes ~4-6 minutes.

---

## Release strategy

| Tag format       | What happens                          |
|-----------------|---------------------------------------|
| `v1.0.0`        | Full release → TestPyPI → PyPI → GH Release |
| `v1.0.0-beta.1` | Pre-release → TestPyPI only           |
| `v1.0.0-rc.1`   | Release candidate → TestPyPI only     |
| push to `develop`| Dev build → TestPyPI (auto-versioned) |

### Patch release workflow
```bash
# Fix a bug, commit, then:
git tag v1.0.1
git push origin v1.0.1
# → auto-publishes to PyPI in ~5 min
```

### Pre-release workflow
```bash
# Ship a beta for testing:
git tag v1.1.0-beta.1
git push origin v1.1.0-beta.1
# → publishes to TestPyPI only
# Users can test: pip install --index-url https://test.pypi.org/simple/ ememediaforge
```

---

## Verify it worked

```bash
# After the release job completes:
pip install ememediaforge
forge version
# EmemediaForge v1.0.0  by @Ememzyvisuals · Axiveri
```

Your package will appear at: **https://pypi.org/project/ememediaforge/**
