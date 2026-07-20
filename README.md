<div align="center">

<h1>EmemediaForge</h1>

**Turn any Speech AI model into a polished showcase video — with one command.**

[![CI](https://github.com/Ememzyvisuals/ememediaforge/actions/workflows/ci.yml/badge.svg)](https://github.com/Ememzyvisuals/ememediaforge/actions)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://pypi.org/project/ememediaforge/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Built by @Ememzyvisuals](https://img.shields.io/badge/built%20by-%40Ememzyvisuals-8B5CF6)](https://github.com/Ememzyvisuals)
[![Axiveri](https://img.shields.io/badge/org-Axiveri-FF6B35)](https://huggingface.co/Axiveri)

*An open source contribution to the global AI community by [Emmanuel Ariyo (@Ememzyvisuals)](https://github.com/Ememzyvisuals), Axiveri.*

</div>

---

## What Is EmemediaForge?

EmemediaForge is a **CPU-only, open source Python CLI tool** that converts raw audio samples and transcripts into professional MP4 showcase videos for Speech AI models.

No GPU. No cloud. No design skills. Just a YAML file and your audio.

```bash
forge build project.yaml
```

```
dist/
├── demo.mp4        ← ready to upload anywhere
├── thumbnail.png   ← cover image
└── metadata.json   ← build info
```

---

## Who Is It For?

EmemediaForge is built for anyone working in the speech AI space:

- **ML researchers** releasing TTS or ASR models on HuggingFace
- **AI startups** demoing voice products to investors or users
- **Indie developers** building speech tools and sharing them publicly
- **African AI builders** working on low-resource language models (Yoruba, Hausa, Igbo, Pidgin, Swahili, Amharic, etc.)
- **NLP educators** creating course material or tutorial content
- **Open source contributors** who want their model releases to look as good as they perform

---

## Use Cases

### 🎙️ TTS Model Showcase
Display your text-to-speech model converting written text into speech — words highlight karaoke-style in perfect sync with the generated audio. Ideal for HuggingFace model cards, GitHub READMEs, and social media announcements.

### 🎧 ASR / STT Model Showcase
Show your speech recognition model transcribing audio in real time — the predicted transcript is revealed word by word as the audio plays. Powerful for demonstrating accuracy on low-resource or under-represented languages.

### 🌍 Low-Resource Language Documentation
Record audio in any language — Yoruba, Hausa, Igbo, Nigerian Pidgin, Swahili, Twi, Amharic, Kinyarwanda — and generate a video that demonstrates the language with synchronized subtitles. A tool for linguists, language preservationists, and African AI labs.

### 📊 Research Paper Demos
Attach a polished video demo to your arXiv paper, ACL/EMNLP/INTERSPEECH submission, or conference poster. Reviewers and readers respond to seeing a model work, not just reading about it.

### 🏢 AI Startup Product Demo
Use EmemediaForge to build demo videos for investor decks, product landing pages, or sales calls — without a video production budget. Ship a new demo every sprint.

### 🎓 Educational Content
Create explainer videos showing how different voices, accents, or languages sound through a TTS system. Perfect for AI/ML course material, YouTube tutorials, or workshop slides.

### 📣 Social Media & Content Creation
Generate short-form demo videos (1080×1920 for Reels/TikTok, 1080×1080 for Twitter/X, 1280×720 for YouTube/LinkedIn) from the same config file — just change the `resolution` field.

### 📦 Dataset Announcements
Releasing a speech dataset? Generate a video that plays audio samples with their transcripts displayed — gives your dataset a human face before anyone downloads it.

### 🔬 Model Comparison
Run EmemediaForge twice with two different models on the same audio. Stack the outputs in any video editor for a side-by-side quality comparison.

---

## Features

- **Karaoke word sync** — words highlight in real time as audio plays (energy-based, no Whisper needed)
- **Animated waveform** — music-visualizer style bars driven by live audio amplitude
- **Four themes** — `modern`, `light`, `dark`, `minimal`
- **Two templates** — `tts` (text-to-speech) and `stt` (speech-to-text / ASR)
- **Three resolutions** — `1280×720` (YouTube/LinkedIn), `1080×1080` (Twitter/Instagram), `1080×1920` (TikTok/Reels)
- **Multiple samples** — showcase as many voices or clips as needed in one video
- **Intro + outro scenes** — branded fade-in/fade-out with logo, title, URL
- **Thumbnail export** — high-res PNG of the intro scene
- **Metadata JSON** — structured build info for CI/CD pipelines
- **Zero GPU required** — runs on laptops, GitHub Actions free tier, Kaggle, Colab
- **Language agnostic** — works for any language, including tonal and low-resource languages
- **Optional high-accuracy alignment** — install `stable-ts` extra for Whisper-powered word timing

---

## Install

**Requires [FFmpeg](https://ffmpeg.org/download.html) installed on your system.**

```bash
# macOS
brew install ffmpeg

# Ubuntu / Debian / Colab / Kaggle
sudo apt install ffmpeg -y

# Windows — download from https://ffmpeg.org/download.html and add to PATH
```

**Install EmemediaForge:**

```bash
git clone https://github.com/Ememzyvisuals/ememediaforge.git
cd ememediaforge
pip install .
```

**Or install directly from a release (no git required):**
```bash
pip install https://github.com/Ememzyvisuals/ememediaforge/releases/download/v1.0.0/ememediaforge-1.0.0-py3-none-any.whl
```

**Or pin to a specific version:**
```bash
pip install git+https://github.com/Ememzyvisuals/ememediaforge.git@v1.0.0
```

---

## Quick Start

```bash
# Scaffold a new project
forge init my-model-demo
cd my-model-demo
```

Drop your audio and transcript files into `samples/`, then edit `project.yaml`:

```yaml
project:
  name: NaijaVox 2.0
  description: Multilingual Nigerian Speech Recognition
  author: Axiveri
  url: https://huggingface.co/Axiveri/NaijaVox-2.0

theme: dark
template: stt
logo: logo.png
resolution: 1280x720
fps: 30

samples:
  - title: Yoruba Sample
    audio: samples/yoruba.wav
    transcript: samples/yoruba.txt
    language: yo

  - title: Nigerian Pidgin
    audio: samples/pidgin.wav
    transcript: samples/pidgin.txt
    language: pcm
```

Validate your config first:
```bash
forge validate project.yaml
```

Then build:
```bash
forge build project.yaml
```

---

## Commands

| Command | Description |
|---------|-------------|
| `forge init [dir]` | Scaffold a new project with example config and folder structure |
| `forge validate <config>` | Check config + verify all asset files exist — no build triggered |
| `forge build <config>` | Full render: audio analysis → alignment → frames → FFmpeg → MP4 |
| `forge build <config> --stable-ts` | Same, but uses Whisper-tiny for higher-accuracy word alignment |
| `forge build <config> --output ./out` | Override output directory |
| `forge version` | Print installed version |

---

## Themes

Set with `theme:` in `project.yaml`.

### `dark` — Near-black · Neon green accent
```
bg #08080C   accent #00FF88   text #FFFFFF
```
Best for: AI model launches, X/Twitter posts, high-impact social content.

### `light` — Pure white · Electric blue accent
```
bg #FFFFFF   surface #F0F4FF   accent #2563EB   text #0F172A
```
Best for: HuggingFace model cards, academic demos, LinkedIn posts, clean screenshots.

### `modern` — White · Deep purple accent
```
bg #FFFFFF   accent #7C3AED   text #111827
```
Best for: Professional demos, product pages, conference talks.

### `minimal` — Off-white · Pure black accent
```
bg #FAFAFA   accent #000000   text #000000
```
Best for: Research papers, academic presentations, print-adjacent content.

---

## Templates

### `tts` — Text-to-Speech
Words from the transcript are highlighted one by one as the model speaks them. The transcript is what the model received as input text.

### `stt` — Speech-to-Text / ASR
The predicted transcript is revealed progressively as the audio plays. The transcript is what the model output from the audio.

---

## Configuration Reference

```yaml
project:
  name:        "Model Name"          # displayed as the headline
  description: "Short description"   # subtitle in intro/outro
  author:      "Author or Org"       # footer attribution
  url:         "https://..."         # HuggingFace or GitHub URL

theme:      dark          # dark | light | modern | minimal
template:   tts           # tts | stt
logo:       logo.png      # optional PNG logo (transparent background recommended)
resolution: 1280x720      # 1280x720 | 1080x1080 | 1080x1920
fps:        30            # 24 | 25 | 30 | 50 | 60

samples:
  - title:      "Voice Label"         # shown on screen
    audio:      samples/audio.wav     # .wav .mp3 .flac .ogg .m4a .aac
    transcript: samples/text.txt      # plain UTF-8 text file
    language:   en                    # BCP-47 code: en yo ha ig pcm sw am …
```

---

## Supported Audio Formats

| Format | Extension |
|--------|-----------|
| WAV *(recommended)* | `.wav` |
| MP3 | `.mp3` |
| FLAC | `.flac` |
| OGG | `.ogg` |
| M4A | `.m4a` |
| AAC | `.aac` |

WAV is recommended for cleanest waveform analysis and fastest processing.

---

## Word Alignment

EmemediaForge ships a **zero-dependency energy-based aligner** — no model download, no GPU, no internet, works offline. It analyzes audio amplitude to detect voiced segments and distributes transcript words proportionally.

This approach is language-agnostic and works reliably for tonal and low-resource languages where standard ML aligners (MFA, Whisper) often fail.

**For higher-accuracy alignment** (English, code-switching, fast speech):
```bash
pip install "ememediaforge[stable_ts]"
forge build project.yaml --stable-ts
```

This downloads a ~150MB Whisper tiny model on first use. CPU-compatible.

See [`docs/ALIGNMENT.md`](docs/ALIGNMENT.md) for full details.

---

## Kaggle / Colab

```python
!apt install ffmpeg -y -q
!pip install git+https://github.com/Ememzyvisuals/ememediaforge.git -q
!forge build project.yaml
```

---

## Performance

All rendering runs on CPU. No GPU required.

| Video Length | Samples | Approx. Render Time |
|-------------|---------|---------------------|
| ~10s | 2 | 30–60 seconds |
| ~30s | 4 | 2–3 minutes |
| ~60s | 6 | 5–8 minutes |

Render time scales with video duration × resolution. `1280×720` renders roughly 2× faster than `1080×1080`.

---

## Development Setup

```bash
git clone https://github.com/Ememzyvisuals/ememediaforge.git
cd ememediaforge
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Lint
ruff check ememediaforge/
```

---

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Areas where contributions are especially valued:
- New themes
- New templates (e.g. model comparison, evaluation display)
- Better alignment for specific language families
- Windows testing and bug reports
- Documentation improvements

---

## Roadmap

- [ ] v1.1 — Custom theme via `project.yaml`
- [ ] v1.1 — SRT subtitle file export
- [ ] v1.1 — Audio normalization pass before render
- [ ] v1.2 — Side-by-side model comparison template
- [ ] v1.2 — WebM export option
- [ ] v2.0 — GPU-accelerated rendering

See [CHANGELOG.md](CHANGELOG.md) for release history.

---

## License

[MIT](LICENSE) © 2025 Emmanuel Ariyo ([@Ememzyvisuals](https://github.com/Ememzyvisuals)), Axiveri.

---

<div align="center">

Built with purpose for the African AI ecosystem and the global speech AI community.

**[@Ememzyvisuals](https://github.com/Ememzyvisuals)** · **[Axiveri](https://huggingface.co/Axiveri)** · **[NaijaVox](https://huggingface.co/Axiveri)** · **[Africlaude](https://huggingface.co/Axiveri)**

</div>
