"""
EmemediaForge — Main pipeline orchestrator.

Execution order:
  1  Load + validate YAML config
  2  Verify all asset files exist
  3  Load audio + compute durations
  4  Align transcript words to audio timestamps
  5  Build video timeline (scenes + audio offsets)
  6  Render all frames → stream to FFmpeg → MP4
  7  Generate thumbnail PNG
  8  Write metadata JSON
"""

from __future__ import annotations

import time
from collections.abc import Callable

from rich.console import Console
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from ememediaforge.alignment.aligner import align
from ememediaforge.audio.analyzer import get_duration
from ememediaforge.config.loader import validate_assets_exist
from ememediaforge.config.schema import ProjectConfig
from ememediaforge.core.exceptions import AssetNotFoundError
from ememediaforge.exporters.metadata import export_metadata
from ememediaforge.exporters.mp4 import export_mp4
from ememediaforge.exporters.thumbnail import generate_thumbnail
from ememediaforge.themes.base import get_theme
from ememediaforge.timeline.scheduler import build_timeline

console = Console()


def run_pipeline(
    config: ProjectConfig,
    use_stable_ts: bool = False,
    on_progress: Callable[[int, int], None] | None = None,
) -> dict:
    """
    Run the full EmemediaForge build pipeline.

    Parameters
    ----------
    config        : validated ProjectConfig
    use_stable_ts : if True, attempt to use stable-ts for alignment
    on_progress   : optional callback(current_frame, total_frames)

    Returns
    -------
    dict with keys: video_path, thumbnail_path, metadata_path, duration
    """
    t_start = time.perf_counter()

    # ── Step 1: Asset validation ─────────────────────────────────────────────
    console.print("[bold cyan]  Checking assets…[/]")
    errors = validate_assets_exist(config)
    if errors:
        raise AssetNotFoundError("Missing assets:\n" + "\n".join(f"  • {e}" for e in errors))

    # ── Step 2: Theme ────────────────────────────────────────────────────────
    theme = get_theme(config.theme)
    width, height = config.get_resolution_tuple()
    console.print(
        f"  Theme: [bold]{theme.name}[/]  |  Resolution: {width}×{height}  |  FPS: {config.fps}"
    )

    # ── Step 3: Audio durations ──────────────────────────────────────────────
    console.print("[bold cyan]  Loading audio…[/]")
    sample_durations: dict[int, float] = {}
    for i, sample in enumerate(config.samples):
        dur = get_duration(sample.audio)
        sample_durations[i] = dur
        console.print(f"    [{i + 1}] {sample.title}: {dur:.2f}s")

    # ── Step 4: Word alignment ───────────────────────────────────────────────
    console.print("[bold cyan]  Aligning transcripts…[/]")
    sample_words = {}
    for i, sample in enumerate(config.samples):
        transcript_text = sample.transcript.read_text(encoding="utf-8").strip()
        words = align(
            audio_path=sample.audio,
            transcript=transcript_text,
            use_stable_ts=use_stable_ts,
        )
        sample_words[i] = words
        console.print(f"    [{i + 1}] {sample.title}: {len(words)} words aligned")

    # ── Step 5: Build timeline ───────────────────────────────────────────────
    console.print("[bold cyan]  Building timeline…[/]")
    timeline = build_timeline(config, sample_durations, sample_words)
    total_dur = timeline.total_duration
    total_frames = int(total_dur * config.fps) + 1
    console.print(f"  Total duration: {total_dur:.2f}s  |  Total frames: {total_frames:,}")

    # ── Step 6: Render MP4 ───────────────────────────────────────────────────
    output_dir = config.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    mp4_path = output_dir / "demo.mp4"

    console.print(f"[bold cyan]  Rendering → {mp4_path}[/]")

    rendered = [0]

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
        transient=True,
    ) as prog:
        task = prog.add_task("  Rendering frames…", total=total_frames)

        def _on_progress(current: int, total: int):
            prog.update(task, completed=current)
            rendered[0] = current
            if on_progress:
                on_progress(current, total)

        export_mp4(
            timeline=timeline,
            theme=theme,
            width=width,
            height=height,
            fps=config.fps,
            output_path=mp4_path,
            on_progress=_on_progress,
        )

    # ── Step 7: Thumbnail ────────────────────────────────────────────────────
    thumb_path = output_dir / "thumbnail.png"
    console.print(f"[bold cyan]  Generating thumbnail → {thumb_path}[/]")
    generate_thumbnail(
        theme=theme,
        width=width,
        height=height,
        title=config.project.name,
        description=config.project.description,
        logo=str(config.logo) if config.logo else None,
        url=config.project.url,
        output_path=thumb_path,
    )

    # ── Step 8: Metadata ─────────────────────────────────────────────────────
    meta_path = output_dir / "metadata.json"
    meta = export_metadata(config, timeline, meta_path, mp4_path, thumb_path)

    elapsed = time.perf_counter() - t_start
    console.print(f"\n[bold green]  ✓ Done in {elapsed:.1f}s[/]")
    console.print(f"    {mp4_path}")
    console.print(f"    {thumb_path}")
    console.print(f"    {meta_path}")

    return {
        "video_path": mp4_path,
        "thumbnail_path": thumb_path,
        "metadata_path": meta_path,
        "duration": total_dur,
        "elapsed_sec": elapsed,
        "metadata": meta,
    }
