"""
EmemediaForge — `forge build` command.
"""

from __future__ import annotations

import sys

from rich.console import Console

from ememediaforge.core.exceptions import ForgeError
from ememediaforge.render.ffmpeg import FFmpegError, check_ffmpeg

console = Console()


def run_build(
    config_path: str,
    stable_ts: bool = False,
    output_dir: str | None = None,
    fast: bool = False,
) -> None:
    """
    Full build: load config → render pipeline → MP4 + thumbnail + metadata.

    Parameters
    ----------
    config_path : path to project.yaml
    stable_ts   : use stable-ts for higher-quality word alignment
    output_dir  : override output directory from config
    fast        : use ultrafast FFmpeg preset (CI, Kaggle, quick previews)
    """
    from ememediaforge.config.loader import load_config
    from ememediaforge.core.pipeline import run_pipeline

    # ── Pre-flight FFmpeg check ──────────────────────────────────────────────
    try:
        check_ffmpeg()
    except FFmpegError as e:
        console.print(f"\n[bold red]✗ FFmpeg not found[/]\n{e}")
        sys.exit(1)

    console.print("\n[bold magenta]EmemediaForge[/] [dim]— Speech AI Showcase Generator[/]")
    if fast:
        console.print("[dim]  Mode: fast (ultrafast FFmpeg preset)[/]")
    console.print(f"[dim]Building[/] [bold cyan]{config_path}[/]\n")

    # ── Load config ──────────────────────────────────────────────────────────
    try:
        config = load_config(config_path)
    except ForgeError as e:
        console.print(f"[bold red]✗ Config error:[/]\n{e}")
        sys.exit(1)

    if output_dir:
        from pathlib import Path

        config.output_dir = Path(output_dir)

    # ── Run pipeline ─────────────────────────────────────────────────────────
    try:
        result = run_pipeline(config, use_stable_ts=stable_ts, fast=fast)
    except ForgeError as e:
        console.print(f"\n[bold red]✗ Build failed:[/]\n{e}")
        sys.exit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Build cancelled.[/]")
        sys.exit(130)

    # ── Summary ──────────────────────────────────────────────────────────────
    console.print(
        f"\n[bold green]✓ Build complete[/] "
        f"({result['elapsed_sec']:.1f}s, "
        f"{result['duration']:.1f}s video)\n"
    )
    console.print(f"  [bold]Video    :[/] {result['video_path']}")
    console.print(f"  [bold]Thumbnail:[/] {result['thumbnail_path']}")
    console.print(f"  [bold]Metadata :[/] {result['metadata_path']}")
    console.print()
