"""
EmemediaForge — FFmpeg subprocess wrapper.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from ememediaforge.core.exceptions import FFmpegError


def check_ffmpeg() -> str:
    """Return ffmpeg binary path. Raises FFmpegError if not found."""
    path = shutil.which("ffmpeg")
    if not path:
        raise FFmpegError(
            "FFmpeg not found in PATH.\n"
            "Install it:\n"
            "  macOS  : brew install ffmpeg\n"
            "  Ubuntu : sudo apt install ffmpeg\n"
            "  Windows: https://ffmpeg.org/download.html"
        )
    return path


def get_ffmpeg_version() -> str:
    """Return FFmpeg version string."""
    ffmpeg = check_ffmpeg()
    result = subprocess.run([ffmpeg, "-version"], capture_output=True, text=True)
    return result.stdout.split("\n")[0]


def build_video_cmd(
    width: int,
    height: int,
    fps: int,
    audio_timings: list[tuple[str, float]],
    output_path: Path,
) -> list[str]:
    """
    Build the FFmpeg command to encode raw RGB frames + mixed audio.

    Parameters
    ----------
    width, height   : video resolution
    fps             : frames per second
    audio_timings   : list of (audio_file_path, start_time_seconds)
    output_path     : destination MP4 path

    Returns
    -------
    list[str] — the complete ffmpeg command
    """
    ffmpeg = check_ffmpeg()

    cmd = [
        ffmpeg,
        "-y",
        # Video input from stdin (raw RGB24)
        "-f",
        "rawvideo",
        "-vcodec",
        "rawvideo",
        "-s",
        f"{width}x{height}",
        "-pix_fmt",
        "rgb24",
        "-r",
        str(fps),
        "-i",
        "pipe:0",
    ]

    # Add audio inputs
    for audio_path, _ in audio_timings:
        cmd.extend(["-i", str(audio_path)])

    # Build filter_complex for audio delay + mix
    if audio_timings:
        filter_parts: list[str] = []
        for i, (_, start_t) in enumerate(audio_timings):
            delay_ms = int(start_t * 1000)
            filter_parts.append(f"[{i + 1}:a]adelay={delay_ms}|{delay_ms},apad[a{i}]")
        n = len(audio_timings)
        mix_in = "".join(f"[a{i}]" for i in range(n))
        filter_parts.append(f"{mix_in}amix=inputs={n}:normalize=0:dropout_transition=0[aout]")
        cmd.extend(
            [
                "-filter_complex",
                ";".join(filter_parts),
                "-map",
                "0:v",
                "-map",
                "[aout]",
            ]
        )
    else:
        cmd.extend(["-map", "0:v"])

    cmd.extend(
        [
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "18",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-ar",
            "44100",
            "-movflags",
            "+faststart",
            str(output_path),
        ]
    )

    return cmd


class FFmpegEncoder:
    """
    Context manager that opens an FFmpeg subprocess accepting raw RGB frames
    on stdin and writes the encoded MP4 to disk.

    Usage:
        with FFmpegEncoder(cmd) as enc:
            for frame in frames:
                enc.write(frame.tobytes())
    """

    def __init__(self, cmd: list[str]):
        self.cmd = cmd
        self._proc: subprocess.Popen | None = None

    def __enter__(self) -> FFmpegEncoder:
        self._proc = subprocess.Popen(
            self.cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
        return self

    def write(self, frame_bytes: bytes) -> None:
        if self._proc and self._proc.stdin:
            try:
                self._proc.stdin.write(frame_bytes)
            except BrokenPipeError as e:
                stderr = (
                    self._proc.stderr.read().decode(errors="replace") if self._proc.stderr else ""
                )
                raise FFmpegError(f"FFmpeg pipe broken:\n{stderr}") from e

    def __exit__(self, *_) -> None:
        if not self._proc:
            return
        if self._proc.stdin:
            self._proc.stdin.close()
        self._proc.wait()
        if self._proc.returncode != 0:
            stderr = (self._proc.stderr.read() if self._proc.stderr else b"").decode(
                errors="replace"
            )
            raise FFmpegError(f"FFmpeg exited with code {self._proc.returncode}:\n{stderr}")
