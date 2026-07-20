"""
EmemediaForge — WordTimestamp data structure.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class WordTimestamp:
    """Maps a single transcript word to its audio time range."""

    word: str
    start: float  # seconds
    end: float  # seconds

    @property
    def duration(self) -> float:
        return max(0.0, self.end - self.start)

    def is_active(self, t: float) -> bool:
        """True if playback time t falls within this word."""
        return self.start <= t < self.end

    def is_past(self, t: float) -> bool:
        return t >= self.end

    def is_future(self, t: float) -> bool:
        return t < self.start
