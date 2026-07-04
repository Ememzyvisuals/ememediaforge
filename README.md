<div align="center">

# EmemediaForge

**Professional showcase video generator for Speech AI models.**

[![PyPI version](https://img.shields.io/pypi/v/ememediaforge.svg)](https://pypi.org/project/ememediaforge/)
[![Python](https://img.shields.io/pypi/pyversions/ememediaforge.svg)](https://pypi.org/project/ememediaforge/)
[![CI](https://github.com/Ememzyvisuals/ememediaforge/actions/workflows/ci.yml/badge.svg)](https://github.com/Ememzyvisuals/ememediaforge/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Built by @Ememzyvisuals](https://img.shields.io/badge/built%20by-%40Ememzyvisuals-8B5CF6.svg)](https://github.com/Ememzyvisuals)

> One command. One YAML file. A polished AI demo video.

**Built for HuggingFace releases · GitHub demos · X/Twitter · LinkedIn · YouTube**

</div>

---

## What Is EmemediaForge?

EmemediaForge converts your raw **audio samples + transcripts** into professional,
shareable MP4 showcase videos — the kind you see on top HuggingFace model pages.

It handles:
- **Karaoke-style word highlighting** synchronized to audio
- **Animated waveform visualization** (music-visualizer bars)
- **Multiple samples** with smooth crossfade transitions
- **Intro + outro scenes** with your branding
- **Thumbnail generation** (great for YouTube / HuggingFace)
- **Three visual themes**: `modern`, `dark`, `minimal`
- **Two templates**: `tts` (Text-to-Speech) and `stt` (Speech-to-Text)

```
forge build project.yaml
```

Outputs:
```
dist/
├── demo.mp4          ← Upload directly to HuggingFace / YouTube
├── thumbnail.png     ← Cover image
└── metadata.json     ← Build metadata
```

---

## Quick Start

### 1. Install

```bash
pip install ememediaforge
```

**Requires FFmpeg** (separate install):

| Platform | Command |
|----------|---------|
| macOS    | `brew install ffmpeg` |
| Ubuntu   | `sudo apt install ffmpeg` |
| Windows  | [ffmpeg.org/download](https://ffmpeg.org/download.html) |

### 2. Scaffold a project

```bash
forge init my-model-demo
cd my-model-demo
```

This creates:
```
my-model-demo/
├── project.yaml        ← Edit this
└── samples/
    ├── sample1.txt
    └── sample2.txt
```

### 3. Add your files

Place your audio files and transcripts in `samples/`:
```
samples/
├── female_voice.wav
├── female_voice.txt   ← plain text transcript
├── male_voice.wav
└── male_voice.txt
```

### 4. Configure `project.yaml`

```yaml
project:
  name: NaijaVox 2.0
  description: Multilingual Nigerian Speech Recognition
  author: Axiveri
  url: https://huggingface.co/Axiveri/NaijaVox-2.0

theme: dark          # modern | dark | minimal
template: stt        # tts | stt
logo: logo.png       # optional PNG logo

resolution: 1280x720  # 1280x720 | 1080x1080 | 1080x1920
fps: 30

samples:
  - title: Yoruba Sample
    audio: samples/yoruba.wav
    transcript: samples/yoruba.txt
    language: yo

  - title: Hausa Sample
    audio: samples/hausa.wav
    transcript: samples/hausa.txt
    language: ha

  - title: Nigerian Pidgin
    audio: samples/pidgin.wav
    transcript: samples/pidgin.txt
    language: pcm
```

### 5. Build

```bash
forge build project.yaml
```

---

## Command Reference

### `forge init [directory]`

Scaffold a new project in the given directory (defaults to current directory).

```bash
forge init .                  # current directory
forge init my-model-demo      # create new directory
```

Downloads the **Inter** grotesk font to `~/.ememediaforge/fonts/` for best visual results.

---

### `forge validate <config>`

Validate your `project.yaml` **without** building anything. Checks:
- Valid YAML syntax
- All required fields present
- All audio and transcript files exist
- Theme and template names are valid

```bash
forge validate project.yaml
```

Example output:
```
Validating project.yaml

  Project      NaijaVox 2.0
  Theme        dark
  Template     stt
  Resolution   1280x720
  FPS          30
  Samples      2

  Samples:
    [1] Yoruba Sample
        audio      ✓ samples/yoruba.wav
        transcript ✓ samples/yoruba.txt
    [2] Hausa Sample
        audio      ✓ samples/hausa.wav
        transcript ✓ samples/hausa.txt

  ✓ Config is valid — ready to build.
  Run: forge build project.yaml
```

---

### `forge build <config>`

Full render pipeline. Flags:

| Flag | Default | Description |
|------|---------|-------------|
| `--stable-ts` | off | Use `stable-ts` for precise word alignment (requires extra install) |
| `--output DIR` | from config | Override the output directory |

```bash
# Standard build
forge build project.yaml

# High-accuracy alignment
forge build project.yaml --stable-ts

# Custom output directory
forge build project.yaml --output ./releases/v2
```

---

### `forge version`

```bash
forge version
# EmemediaForge v1.0.0  by Axiveri (Emmanuel Ariyo)
```

---

## Project Configuration Reference

Full `project.yaml` schema:

```yaml
# ── Project Metadata ──────────────────────────────────────────────────────────
project:
  name:        "Model Name"          # required — displayed as headline
  description: "Short description"   # optional — shown in intro/outro
  author:      "Your Name"           # optional — footer attribution
  url:         "https://..."         # optional — HuggingFace or GitHub URL

# ── Visual Settings ───────────────────────────────────────────────────────────
theme:      modern      # modern | dark | minimal
template:   tts         # tts | stt
logo:       logo.png    # optional PNG/JPG (transparent PNG recommended)
resolution: 1280x720    # 1280x720 | 1080x1080 | 1080x1920
fps:        30          # 24 | 25 | 30 | 50 | 60

# ── Audio Samples ─────────────────────────────────────────────────────────────
samples:
  - title:      "Display Label"          # shown on-screen
    audio:      samples/audio.wav        # .wav .mp3 .flac .ogg .m4a .aac
    transcript: samples/transcript.txt   # plain .txt file
    language:   en                       # BCP-47 code (en, yo, ha, ig, pcm…)
```

### Resolution Guide

| Resolution | Use Case |
|------------|---------|
| `1280x720` | YouTube, LinkedIn, GitHub (recommended) |
| `1080x1080`| Twitter/X square, Instagram |
| `1080x1920`| TikTok, YouTube Shorts, Reels |

---

## Themes

### `dark` — Neon Green on Near-Black
Best for: AI model demos, tech audiences, NaijaVox/Africlaude showcase
```
bg: #08080C    accent: #00FF88    text: #FFFFFF
```

### `light` — Electric Blue on White  *(default for light environments)*
Best for: HuggingFace model cards, academic demos, LinkedIn, clean screenshots
```
bg: #FFFFFF    surface: #F0F4FF    accent: #2563EB    text: #0F172A
```

### `modern` — Purple on White
Best for: Professional demos, HuggingFace model pages, LinkedIn
```
bg: #FFFFFF    accent: #7C3AED    text: #111827
```

### `minimal` — Black on Off-White
Best for: Clean academic demos, papers, conservative audiences
```
bg: #FAFAFA    accent: #000000    text: #000000
```

---

## Templates

### `tts` — Text-to-Speech Showcase

Shows your TTS model converting text → speech:
- Karaoke words highlight as the voice speaks them
- Each word is tracked by the energy-based alignment engine
- Great for: Kokoro, NaijaVox, XTTS, Bark, ElevenLabs alternatives

### `stt` — Speech-to-Text Showcase

Shows your STT/ASR model transcribing audio → text:
- Transcript words reveal progressively as audio plays
- Progress bar shows how far through the audio we are
- Great for: Whisper fine-tunes, NaijaVox ASR, custom STT models

---

## Word Alignment Engine

EmemediaForge ships a **zero-dependency alignment engine** — no Whisper download,
no GPU, no internet required.

### How it works

1. Load audio with `librosa`
2. Compute RMS energy envelope (512-sample hop)
3. Detect voiced segments (energy > 12% of peak)
4. Distribute words proportionally by character count across voiced speech
5. Add short inter-word gaps for natural timing

This produces smooth karaoke effects for all languages, including
Nigerian languages (Yoruba, Hausa, Igbo, Pidgin English) where
ML-based aligners often fail.

### Optional: High-accuracy alignment

For production demos where precise alignment matters, install `stable-ts`:

```bash
pip install "ememediaforge[stable_ts]"
forge build project.yaml --stable-ts
```

This downloads a 150MB Whisper tiny model on first use and uses it for
word-level forced alignment. Results are noticeably better for fast speech.

---

## Audio Formats

| Format | Extension | Notes |
|--------|-----------|-------|
| WAV | `.wav` | Recommended — lossless, no decode overhead |
| MP3 | `.mp3` | Widely supported |
| FLAC | `.flac` | Lossless compressed |
| OGG  | `.ogg` | Open format |
| M4A  | `.m4a` | AAC in container |
| AAC  | `.aac` | Raw AAC |

**Recommended**: Export from your TTS model as WAV (16-bit or 32-bit, any sample rate).

---

## Fonts

EmemediaForge uses **Inter** (a neo-grotesque sans-serif by Rasmus Andersson)
as the primary font. Run `forge init` to download it automatically.

Fallback chain:
1. Inter Regular/Bold (downloaded via `forge init`)
2. Liberation Sans (bundled, similar to Arial — grotesk)
3. DejaVu Sans (bundled, humanist sans)
4. PIL default bitmap font

---

## File Structure

```
ememediaforge/
├── pyproject.toml
├── README.md
├── LICENSE
│
└── ememediaforge/
    ├── cli/           ← Typer CLI commands (build, validate, init)
    ├── config/        ← Pydantic v2 schema + YAML loader
    ├── assets/        ← Font manager + bundled fonts
    │   └── fonts/     ← LiberationSans, DejaVu (bundled)
    ├── audio/         ← librosa-based audio analysis
    ├── alignment/     ← Word-to-audio timestamp alignment
    ├── timeline/      ← Scene timeline builder + scheduler
    ├── scenes/        ← IntroScene, SampleScene, TransitionScene, OutroScene
    ├── themes/        ← modern, dark, minimal theme definitions
    ├── render/        ← FFmpeg wrapper + frame compositor + encoder
    ├── exporters/     ← MP4, thumbnail, metadata exporters
    └── core/          ← Pipeline orchestrator + exceptions
```

---

## Performance

| Video Length | Samples | Render Time (CPU) |
|-------------|---------|-------------------|
| ~10s        | 2       | ~30–60s           |
| ~30s        | 4       | ~90–180s          |
| ~60s        | 6       | ~3–6 min          |

Render time scales linearly with video duration × resolution.
1280×720 is ~2× faster than 1080×1080.

---

## Deployment / Publishing

### HuggingFace Model Card

```markdown
## Demo

https://huggingface.co/your-org/your-model/resolve/main/demo.mp4
```

Or use the HuggingFace Python client:

```python
from huggingface_hub import HfApi

api = HfApi()
api.upload_file(
    path_or_fileobj="dist/demo.mp4",
    path_in_repo="demo.mp4",
    repo_id="your-org/your-model",
    repo_type="model",
)
api.upload_file(
    path_or_fileobj="dist/thumbnail.png",
    path_in_repo="thumbnail.png",
    repo_id="your-org/your-model",
    repo_type="model",
)
```

### GitHub Release

```bash
gh release create v1.0 dist/demo.mp4 dist/thumbnail.png \
  --title "Model v1.0" \
  --notes "See demo.mp4 for audio samples."
```

### CI/CD with GitHub Actions

```yaml
# .github/workflows/demo.yml
name: Build Demo Video

on:
  push:
    tags: ["v*"]

jobs:
  build-demo:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install FFmpeg
        run: sudo apt-get install -y ffmpeg

      - name: Install Python deps
        run: pip install ememediaforge

      - name: Build demo video
        run: forge build project.yaml

      - name: Upload to HuggingFace
        env:
          HF_TOKEN: ${{ secrets.HF_TOKEN }}
        run: |
          pip install huggingface_hub
          python -c "
          from huggingface_hub import HfApi
          import os
          api = HfApi(token=os.environ['HF_TOKEN'])
          api.upload_file('dist/demo.mp4',   'demo.mp4',      'your-org/your-model')
          api.upload_file('dist/thumbnail.png', 'thumbnail.png', 'your-org/your-model')
          "
```

---

## Publishing — Fully Automated via GitHub Actions

Releases are **zero-touch** after one-time setup. See [`docs/PYPI_CICD_SETUP.md`](docs/PYPI_CICD_SETUP.md) for the one-time configuration.

After setup, shipping a release is one command:

```bash
# Patch release
make release v=1.0.1

# Or manually:
git tag v1.0.1 && git push origin v1.0.1
```

GitHub Actions handles everything:
1. Runs full test matrix ✓
2. Builds `dist/*.whl` + `dist/*.tar.gz` ✓
3. Publishes to TestPyPI → verifies install ✓
4. Publishes to PyPI via OIDC (zero API tokens) ✓
5. Creates GitHub Release with auto-generated changelog ✓

**Pre-release (beta → TestPyPI only):**
```bash
make release-beta v=1.1.0-beta.1
```

---

## Development Setup

```bash
git clone https://github.com/Ememzyvisuals/ememediaforge.git
cd ememediaforge

# Install in editable mode with dev extras
pip install -e ".[dev]"

# Run tests
pytest

# Lint
ruff check .

# Type check
mypy ememediaforge/
```

---

## Dependency Versions (Pinned & Tested)

| Package | Version | Role |
|---------|---------|------|
| `librosa` | ≥0.11.0 | Audio analysis + waveform |
| `numpy` | ≥1.26.0 | Array operations |
| `pydantic` | ≥2.5.0 | Config schema validation |
| `PyYAML` | ≥6.0.1 | YAML parsing |
| `pillow` | ≥10.3.0 | Frame rendering |
| `scipy` | ≥1.11.0 | Signal processing |
| `soundfile` | ≥0.12.1 | Audio I/O |
| `typer` | ≥0.12.0 | CLI framework |
| `rich` | ≥13.7.0 | Terminal output |
| FFmpeg | 6.x | Video encoding (system) |

> **Why not `aeneas`?** aeneas supports only Python 2.7–3.6 and is unmaintained.
> EmemediaForge uses a custom energy-based aligner (no ML required) with optional
> `stable-ts` for higher accuracy.

---

## FAQ

**Q: Do I need a GPU?**
No. The default alignment engine runs on CPU with no model downloads.
Optional `--stable-ts` downloads a ~150MB Whisper tiny model (CPU-compatible).

**Q: What languages are supported?**
Any language your audio contains. The energy-based aligner is language-agnostic.
Works great for Yoruba, Hausa, Igbo, Pidgin English, Arabic, Chinese, etc.

**Q: My video has no audio.**
Check that FFmpeg is installed and your audio file paths are correct.
Run `forge validate project.yaml` to check paths first.

**Q: The word timing looks off.**
Try adding `--stable-ts` for higher accuracy alignment (requires extra install).
Also ensure your transcript matches exactly what is spoken in the audio.

**Q: Can I add a custom theme?**
Yes. Subclass `ememediaforge.themes.base.Theme` and pass it directly to the pipeline.
Custom themes via YAML config are planned for v1.1.

**Q: Can I use non-WAV audio?**
Yes: WAV, MP3, FLAC, OGG, M4A, AAC are all supported.
WAV is recommended for best quality and reliability.

---

## Roadmap

- [ ] v1.1: Custom theme via YAML (`theme_custom:` key)
- [ ] v1.1: SRT subtitle export
- [ ] v1.2: Side-by-side comparison template (model A vs model B)
- [ ] v1.2: Audio normalization pass before rendering
- [ ] v1.3: WebM export option
- [ ] v1.3: Animated logo support (GIF/APNG)
- [ ] v2.0: GPU-accelerated rendering

---

## Contributing

```bash
git clone https://github.com/Ememzyvisuals/ememediaforge.git
pip install -e ".[dev]"
```

Please open an issue before submitting large PRs. See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

MIT © 2025 [Emmanuel Ariyo / Axiveri](https://github.com/Ememzyvisuals)

---

<div align="center">

Built with ❤️ for the African AI ecosystem.

**[@Ememzyvisuals](https://github.com/Ememzyvisuals)** · **[NaijaVox](https://huggingface.co/Axiveri)** · **[Africlaude](https://huggingface.co/Axiveri)**

</div>
