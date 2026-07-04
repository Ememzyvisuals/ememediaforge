# Changelog

All notable changes to EmemediaForge are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [1.0.0] — 2025-07-02

### ✨ Added
- `forge build` — full render pipeline from single YAML config
- `forge validate` — validate config + assets without building
- `forge init` — scaffold new project with example files + font download
- Four visual themes: `modern`, `light`, `dark`, `minimal`
- Two video templates: `tts` (Text-to-Speech), `stt` (Speech-to-Text)
- Karaoke-style word highlighting with energy-based word alignment
- Animated mirrored waveform bars (music-visualizer style)
- Animated intro scene with logo + title fade-in
- Animated outro scene with URL + branding
- Crossfade transition between samples
- FFmpeg H.264 pipeline — raw RGB frames streamed to stdin
- Thumbnail PNG export from intro scene at peak visibility
- `metadata.json` export with full build metadata
- Three output resolutions: `1280x720`, `1080x1080`, `1080x1920`
- Zero-dependency energy-based word aligner — works for all languages
  including Yoruba, Hausa, Igbo, Nigerian Pidgin
- Optional `stable-ts` integration for higher-accuracy alignment
- Inter grotesk font auto-download via `forge init`
- Bundled Liberation Sans + DejaVu fallback fonts (no internet required)
- Pydantic v2 schema validation with clear error messages
- Full CI/CD via GitHub Actions (test matrix, OIDC PyPI publish, auto-release)
- 22 unit tests covering all major subsystems

### 📚 Documentation
- Full README with quick start, config reference, theme guide
- `docs/THEMES.md` — visual design guide
- `docs/ALIGNMENT.md` — alignment engine internals
- `docs/DEPLOYMENT.md` — HuggingFace, Docker, GitHub Actions deployment
- `docs/PYPI_CICD_SETUP.md` — one-time OIDC trusted publisher setup

---

## Roadmap

### [1.1.0] — Planned
- Custom theme via YAML config key `theme_custom:`
- SRT subtitle export alongside MP4
- Audio normalization pass (auto-gain before rendering)
- `--watch` flag for live rebuild on file changes

### [1.2.0] — Planned
- Side-by-side comparison template (Model A vs Model B)
- Evaluation template with WER display
- WebM export option

### [2.0.0] — Future
- GPU-accelerated frame rendering
- Cloud render API (EmemediaForge Pro)
- Web UI (HuggingFace Space)
