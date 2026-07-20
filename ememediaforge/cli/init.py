"""
EmemediaForge — `forge init` command.
Creates a starter project structure with example project.yaml.
"""

from __future__ import annotations

from pathlib import Path

from rich.console import Console

console = Console()

EXAMPLE_YAML = """\
# ─────────────────────────────────────────────────────────
# EmemediaForge — Project Configuration
# Run: forge build project.yaml
# ─────────────────────────────────────────────────────────

project:
  name: YourModel 1.0
  description: Short description of your AI model
  author: Your Name / Organization
  url: https://huggingface.co/your-org/your-model

# Visual theme: modern | dark | minimal
theme: dark

# Video template: tts (text-to-speech) | stt (speech-to-text)
template: tts

# Path to your logo (PNG recommended, transparent background)
logo: logo.png

# Output resolution: 1280x720 | 1080x1080 | 1080x1920
resolution: 1280x720

# Frames per second: 24 | 25 | 30 | 50 | 60
fps: 30

# Audio samples to showcase (add as many as needed)
samples:
  - title: Sample Voice 1
    audio: samples/sample1.wav
    transcript: samples/sample1.txt
    language: en   # BCP-47 code: en, yo, ha, ig, pcm …

  - title: Sample Voice 2
    audio: samples/sample2.wav
    transcript: samples/sample2.txt
    language: en
"""

GITIGNORE = """\
dist/
__pycache__/
*.pyc
.DS_Store
"""

README_TEMPLATE = """\
# {name}

{description}

## Demo Video

Generated with [EmemediaForge](https://github.com/Ememzyvisuals/ememediaforge).

## Usage

```bash
pip install ememediaforge
forge build project.yaml
```
"""


def run_init(directory: str = ".") -> None:
    """Scaffold a new EmemediaForge project."""
    proj_dir = Path(directory).resolve()
    proj_dir.mkdir(parents=True, exist_ok=True)
    samples_dir = proj_dir / "samples"
    samples_dir.mkdir(exist_ok=True)

    # Write project.yaml
    yaml_path = proj_dir / "project.yaml"
    if yaml_path.exists():
        console.print("[yellow]  project.yaml already exists, skipping.[/]")
    else:
        yaml_path.write_text(EXAMPLE_YAML, encoding="utf-8")
        console.print(f"  [green]✓[/] Created {yaml_path}")

    # .gitignore
    gi_path = proj_dir / ".gitignore"
    if not gi_path.exists():
        gi_path.write_text(GITIGNORE)
        console.print(f"  [green]✓[/] Created {gi_path}")

    # Placeholder sample files
    for n in (1, 2):
        wav = samples_dir / f"sample{n}.wav"
        txt = samples_dir / f"sample{n}.txt"
        if not txt.exists():
            txt.write_text(f"Replace this with your sample {n} transcript.", encoding="utf-8")
            console.print(f"  [green]✓[/] Created {txt}")
        if not wav.exists():
            console.print(f"  [dim]  Place your audio file at {wav}[/]")

    # Try to download Inter font
    console.print("\n  [bold cyan]Downloading Inter font (grotesk)…[/]")
    try:
        from ememediaforge.assets.loader import FontManager

        ok = FontManager.download_inter(show_progress=True)
        if not ok:
            console.print(
                "  [yellow]  Font download failed — bundled LiberationSans will be used.[/]"
            )
    except Exception as e:
        console.print(f"  [yellow]  Font download skipped: {e}[/]")

    console.print(f"\n[bold green]  Project scaffolded at {proj_dir}[/]")
    console.print("  Next steps:")
    console.print("    1. Add your audio files to [bold]samples/[/]")
    console.print("    2. Edit [bold]project.yaml[/] with your model details")
    console.print("    3. Run [bold cyan]forge build project.yaml[/]")
