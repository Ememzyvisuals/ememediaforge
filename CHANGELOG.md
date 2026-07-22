# Changelog

All notable changes to EmemediaForge are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [1.0.3] — 2026-07-22

### 🐛 Fixed
- `--fast` flag was visible in `forge build --help` after v1.0.2 but was never
  registered as a Typer parameter in `cmd_build`'s signature — the CLI threw
  `No such option: --fast` when used. Complete rewrite of `cli/app.py` and
  `cli/build.py` with `fast: bool = typer.Option(False, "--fast", ...)` properly
  declared in the function signature.

---

## [1.0.2] — 2026-07-22

### ✨ Added
- `--fast` flag for `forge build` — uses FFmpeg `ultrafast` preset, 5–10× faster
  encode with minimal quality difference. Recommended for CI, Kaggle, Colab, and
  quick iteration. CI demo job now uses `forge build --fast`.
- `timeout-minutes: 15` on the `build-demo` CI job — hard cap so no run can
  hang for hours if something goes wrong.

### 🐛 Fixed
- **Critical: FFmpeg stderr pipe deadlock** — the `build-demo` CI job was hanging
  for up to 6 hours and had to be force-cancelled. Root cause: FFmpeg writes logs
  to stderr; when the 64 KB pipe buffer fills up, FFmpeg blocks waiting for the
  parent process to read it; meanwhile the parent process blocks writing the next
  video frame to stdin. Neither side moves. Classic deadlock.

  Fix: `render/ffmpeg.py` — stderr is now drained continuously by a background
  daemon thread (`threading.Thread`) that starts when FFmpeg launches and runs
  until it exits. The stderr pipe buffer never fills. FFmpeg never blocks.

---

## [1.0.1] — 2026-07-21

### 🐛 Fixed
- All 80 ruff lint errors resolved — CI was failing at the lint step
  - 40 `I001` unsorted imports (auto-fixed with `ruff --fix`)
  - 18 `F401` unused imports in `__init__.py` re-exports (fixed via
    `per-file-ignores` config)
  - 9 `UP045` `Optional[X]` type hints (auto-updated to `X | None`)
  - 4 `F841` unused variables in scene renderers (removed manually)
  - 4 `UP035` deprecated `typing` imports (auto-fixed)
  - Others: f-strings without placeholders, redundant open modes
- Fixed `[tool.ruff]` → `[tool.ruff.lint]` config section (deprecated format
  was causing ruff warnings on every run)
- 48 Python files reformatted with `ruff format`
- Fixed year 2025 → 2026 in `LICENSE` and `README.md`
- Removed last PyPI badge URL from README

---

## [1.0.0] — 2026-07-20

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
- Three output resolutions: `1280×720`, `1080×1080`, `1080×1920`
- Zero-dependency energy-based word aligner — language-agnostic,
  works for Yoruba, Hausa, Igbo, Nigerian Pidgin and all other languages
- Optional `stable-ts` integration for Whisper-powered alignment
- Inter grotesk font auto-download via `forge init`
- Bundled Liberation Sans + DejaVu fallback fonts (no internet required)
- Pydantic v2 schema validation with clear error messages
- GitHub Actions CI (test matrix across Python 3.10–3.12 × Ubuntu/macOS/Windows)
- GitHub Actions release pipeline (test → build → demo video → GitHub Release)
- NaijaVox 2.0 demo build in CI with synthetic audio generator
- 22 unit tests covering all major subsystems

### 📚 Documentation
- Full public-facing README — use cases, tips, troubleshooting, theme guide
- `docs/THEMES.md` — visual theme reference
- `docs/ALIGNMENT.md` — alignment engine internals and language support
- `docs/RELEASES.md` — install options and release guide

---

## Roadmap

### [1.1.0] — Planned
- Custom theme via YAML config key `theme_custom:`
- SRT subtitle export alongside MP4
- Audio normalization pass (auto-gain before rendering)
- `--watch` flag for live rebuild on file changes

### [1.2.0] — Planned
- Side-by-side comparison template (Model A vs Model B)
- Evaluation template with WER / CER display
- WebM export option

### [2.0.0] — Future
- GPU-accelerated frame rendering
- Cloud render API (EmemediaForge Pro)
- Web UI (HuggingFace Space)
