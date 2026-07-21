"""
EmemediaForge — FFmpeg subprocess wrapper.

Key design: stderr is drained in a background thread to prevent the
classic pipe buffer deadlock:

  FFmpeg fills stderr buffer (64KB default)
  → FFmpeg blocks waiting for parent to read stderr
  → Parent blocks writing frames to stdin
  → Deadlock — hangs forever

The background thread drains stderr continuously so FFmpeg never blocks.
"""

from __future__ import annotations

import shutil
import subprocess
import threading
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
    fast: bool = False,
) -> list[str]:
    """
    Build the FFmpeg command to encode raw RGB frames + mixed audio.

    Parameters
    ----------
    width, height  : video resolution
    fps            : frames per second
    audio_timings  : list of (audio_file_path, start_time_seconds)
    output_path    : destination MP4 path
    fast           : use ultrafast preset (for CI/testing)
    """
    ffmpeg = check_ffmpeg()
    preset = "ultrafast" if fast else "fast"

    cmd = [
        ffmpeg,
        "-y",
        # Video from stdin (raw RGB24 frames)
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

    # Add each audio input
    for audio_path, _ in audio_timings:
        cmd.extend(["-i", str(audio_path)])

    # Audio delay + mix filter
    if audio_timings:
        parts: list[str] = []
        for i, (_, start_t) in enumerate(audio_timings):
            delay_ms = int(start_t * 1000)
            parts.append(f"[{i + 1}:a]adelay={delay_ms}|{delay_ms},apad[a{i}]")
        n = len(audio_timings)
        mix_in = "".join(f"[a{i}]" for i in range(n))
        parts.append(f"{mix_in}amix=inputs={n}:normalize=0:dropout_transition=0[aout]")
        cmd.extend(
            [
                "-filter_complex",
                ";".join(parts),
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
            preset,
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
    Context manager that streams raw RGB frames to FFmpeg via stdin.

    Stderr is drained continuously in a background daemon thread,
    preventing the pipe buffer deadlock that causes indefinite hangs.

    Usage:
        with FFmpegEncoder(cmd) as enc:
            for frame in frames:
                enc.write(frame.tobytes())
    """

    def __init__(self, cmd: list[str]):
        self.cmd = cmd
        self._proc: subprocess.Popen | None = None
        self._stderr_lines: list[str] = []
        self._stderr_thread: threading.Thread | None = None

    def __enter__(self) -> FFmpegEncoder:
        self._proc = subprocess.Popen(
            self.cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,  # piped so we can capture errors
        )

        # ── Drain stderr in background — prevents pipe buffer deadlock ────────
        def _drain_stderr() -> None:
            assert self._proc and self._proc.stderr
            for line in self._proc.stderr:
                self._stderr_lines.append(line.decode(errors="replace").rstrip())

        self._stderr_thread = threading.Thread(
            target=_drain_stderr,
            daemon=True,
            name="ffmpeg-stderr-drain",
        )
        self._stderr_thread.start()
        return self

    def write(self, frame_bytes: bytes) -> None:
        """Write one frame's raw RGB bytes to FFmpeg stdin."""
        if not (self._proc and self._proc.stdin):
            return
        try:
            self._proc.stdin.write(frame_bytes)
        except BrokenPipeError as e:
            # FFmpeg died — collect stderr and raise a clean error
            if self._stderr_thread:
                self._stderr_thread.join(timeout=3)
            stderr = "\n".join(self._stderr_lines[-20:])  # last 20 lines
            raise FFmpegError(f"FFmpeg pipe broken:\n{stderr}") from e

    def __exit__(self, *_) -> None:
        if not self._proc:
            return

        # Close stdin to signal end of stream
        if self._proc.stdin:
            try:
                self._proc.stdin.close()
            except BrokenPipeError:
                pass

        # Wait for FFmpeg to finish encoding
        self._proc.wait()

        # Let stderr thread finish collecting output
        if self._stderr_thread:
            self._stderr_thread.join(timeout=10)

        if self._proc.returncode != 0:
            stderr = "\n".join(self._stderr_lines[-30:])
            raise FFmpegError(f"FFmpeg exited with code {self._proc.returncode}:\n{stderr}")
