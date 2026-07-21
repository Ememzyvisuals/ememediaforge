"""
EmemediaForge — MP4 export convenience wrapper.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from ememediaforge.render.encoder import encode_video
from ememediaforge.themes.base import Theme
from ememediaforge.timeline.timeline import VideoTimeline


def export_mp4(
    timeline: VideoTimeline,
    theme: Theme,
    width: int,
    height: int,
    fps: int,
    output_path: Path,
    on_progress: Callable[[int, int], None] | None = None,
    fast: bool = False,
) -> Path:
    """Write the final MP4. Returns the output path."""
    return encode_video(
        timeline=timeline,
        theme=theme,
        width=width,
        height=height,
        fps=fps,
        output_path=output_path,
        on_progress=on_progress,
        fast=fast,
    )
