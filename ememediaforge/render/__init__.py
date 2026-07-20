"""EmemediaForge render — compositor, encoder, FFmpeg wrapper."""

from ememediaforge.render.compositor import compose_frames, precompute_waveforms
from ememediaforge.render.encoder import encode_video
from ememediaforge.render.ffmpeg import FFmpegEncoder, build_video_cmd, check_ffmpeg

__all__ = [
    "FFmpegEncoder",
    "check_ffmpeg",
    "build_video_cmd",
    "compose_frames",
    "precompute_waveforms",
    "encode_video",
]
