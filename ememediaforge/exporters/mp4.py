"""
EmemediaForge — MP4 export convenience wrapper.
"""
from __future__ import annotations

from pathlib import Path
from typing import Callable, Optional

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
    on_progress: Optional[Callable[[int, int], None]] = None,
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
    )
