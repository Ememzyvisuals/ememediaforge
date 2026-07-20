"""
EmemediaForge — High-level video encoder.
Ties together compositor + FFmpeg encoder.
"""
from __future__ import annotations
from pathlib import Path
from typing import Callable, Optional

from ememediaforge.render.compositor import compose_frames, precompute_waveforms
from ememediaforge.render.ffmpeg     import build_video_cmd, FFmpegEncoder
from ememediaforge.timeline.timeline import VideoTimeline
from ememediaforge.themes.base       import Theme


def encode_video(
    timeline: VideoTimeline,
    theme: Theme,
    width: int,
    height: int,
    fps: int,
    output_path: Path,
    on_progress: Optional[Callable[[int, int], None]] = None,
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

    Returns
    -------
    Path to the written MP4 file.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Pre-compute waveform data (CPU-bound, done once)
    waveform_cache = precompute_waveforms(timeline, fps)

    # Build FFmpeg command
    audio_timings = timeline.audio_timings()
    cmd = build_video_cmd(width, height, fps, audio_timings, output_path)

    # Stream frames to FFmpeg
    total_frames = int(timeline.total_duration * fps) + 1

    with FFmpegEncoder(cmd) as enc:
        for frame in compose_frames(
            timeline, theme, width, height, fps,
            waveform_cache, on_progress=on_progress
        ):
            enc.write(frame.tobytes())

    return output_path
