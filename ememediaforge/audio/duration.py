"""
EmemediaForge — Lightweight audio duration utilities.
"""

from __future__ import annotations

from pathlib import Path

from ememediaforge.audio.analyzer import get_duration


def get_audio_duration(path: Path | str) -> float:
    """Return audio duration in seconds."""
    return get_duration(path)


def format_duration(seconds: float) -> str:
    """Format seconds as MM:SS string."""
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m:02d}:{s:02d}"
