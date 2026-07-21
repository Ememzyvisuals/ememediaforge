"""
EmemediaForge — High-level video encoder.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from ememediaforge.render.compositor import compose_frames, precompute_waveforms
from ememediaforge.render.ffmpeg import FFmpegEncoder, build_video_cmd
from ememediaforge.themes.base import Theme
from ememediaforge.timeline.timeline import VideoTimeline


def encode_video(
    timeline: VideoTimeline,
    theme: Theme,
    width: int,
    height: int,
    fps: int,
    output_path: Path,
    on_progress: Callable[[int, int], None] | None = None,
    fast: bool = False,
) -> Path:
    """
    Full render pipeline: frames → FFmpeg → MP4.

    Parameters
    ----------
    timeline     : VideoTimeline with all scenes
    theme        : visual theme
    width/height : output resolution
    fps          : frames per second
    output_path  : where to write the .mp4 file
    on_progress  : optional callback(current_frame, total_frames)
    fast         : use ultrafast FFmpeg preset (for CI / quick previews)
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    waveform_cache = precompute_waveforms(timeline, fps)
    audio_timings = timeline.audio_timings()
    cmd = build_video_cmd(width, height, fps, audio_timings, output_path, fast=fast)

    with FFmpegEncoder(cmd) as enc:
        for frame in compose_frames(
            timeline,
            theme,
            width,
            height,
            fps,
            waveform_cache,
            on_progress=on_progress,
        ):
            enc.write(frame.tobytes())

    return output_path
