# EmemediaForge — Deployment Guide

## Local Install

```bash
pip install ememediaforge
forge init my-demo && cd my-demo
# Add audio + transcripts, edit project.yaml
forge build project.yaml
```

---

## PyPI Publishing

```bash
# Build distribution packages
pip install build twine
python -m build

# Check the build
twine check dist/*

# Publish to TestPyPI first
twine upload --repository testpypi dist/*
pip install --index-url https://test.pypi.org/simple/ ememediaforge

# Publish to PyPI
twine upload dist/*
```

---

## HuggingFace Upload

```python
from huggingface_hub import HfApi

api = HfApi(token="hf_YOUR_TOKEN")

# Upload video to model repo
api.upload_file(
    path_or_fileobj="dist/demo.mp4",
    path_in_repo="demo.mp4",
    repo_id="Axiveri/NaijaVox-2.0",
    repo_type="model",
)
api.upload_file(
    path_or_fileobj="dist/thumbnail.png",
    path_in_repo="thumbnail.png",
    repo_id="Axiveri/NaijaVox-2.0",
    repo_type="model",
)
```

Then embed in your model card README.md:
```markdown
## Demo

<video src="https://huggingface.co/Axiveri/NaijaVox-2.0/resolve/main/demo.mp4"
       controls autoplay muted loop></video>
```

---

## GitHub Actions CI/CD

```yaml
# .github/workflows/demo.yml
name: Build Demo Video

on:
  push:
    tags: ["v*"]
  workflow_dispatch:

jobs:
  build-demo:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install FFmpeg
        run: sudo apt-get install -y ffmpeg
      - name: Install EmemediaForge
        run: pip install ememediaforge
      - name: Validate config
        run: forge validate project.yaml
      - name: Build demo
        run: forge build project.yaml
      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: demo-video
          path: dist/
      - name: Publish to HuggingFace
        if: startsWith(github.ref, 'refs/tags/')
        env:
          HF_TOKEN: ${{ secrets.HF_TOKEN }}
        run: |
          python - <<'EOF'
          import os
          from huggingface_hub import HfApi
          api = HfApi(token=os.environ["HF_TOKEN"])
          repo = "Axiveri/NaijaVox-2.0"
          api.upload_file("dist/demo.mp4",       "demo.mp4",       repo)
          api.upload_file("dist/thumbnail.png",  "thumbnail.png",  repo)
          api.upload_file("dist/metadata.json",  "metadata.json",  repo)
          print("Published to HuggingFace!")
          EOF
```

---

## Docker

```dockerfile
FROM python:3.11-slim

# Install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Install EmemediaForge
RUN pip install ememediaforge

WORKDIR /project
COPY . .

CMD ["forge", "build", "project.yaml"]
```

Build and run:
```bash
docker build -t ememediaforge-runner .
docker run -v $(pwd):/project ememediaforge-runner
# dist/ will be created in your current directory
```

---

## Platform Notes

### macOS
```bash
brew install ffmpeg
pip install ememediaforge
```

### Ubuntu / Debian
```bash
sudo apt install ffmpeg
pip install ememediaforge
```

### Windows
1. Download FFmpeg from https://ffmpeg.org/download.html
2. Add `ffmpeg.exe` directory to your `PATH`
3. `pip install ememediaforge`

### Kaggle / Colab
```python
!apt-get install -y ffmpeg -q
!pip install ememediaforge -q
!forge build project.yaml
```
