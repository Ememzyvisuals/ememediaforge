"""
EmemediaForge — Timeline data structures.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SceneSpec:
    """
    Specifies a single scene in the final video timeline.

    Attributes
    ----------
    scene_type  : "intro" | "sample" | "transition" | "outro"
    start_time  : time in seconds where this scene begins in the full video
    duration    : how long this scene lasts in seconds
    data        : scene-specific payload (varies by type)
    """

    scene_type: str
    start_time: float
    duration: float
    data: dict[str, Any] = field(default_factory=dict)

    @property
    def end_time(self) -> float:
        return self.start_time + self.duration

    def local_time(self, global_time: float) -> float:
        """Convert a global video timestamp to this scene's local time (0 → duration)."""
        return max(0.0, min(self.duration, global_time - self.start_time))

    def progress(self, global_time: float) -> float:
        """Return 0.0 → 1.0 progress through this scene."""
        if self.duration <= 0:
            return 1.0
        return self.local_time(global_time) / self.duration


@dataclass
class VideoTimeline:
    """
    Ordered list of scenes that make up the complete video.
    """

    scenes: list[SceneSpec] = field(default_factory=list)

    @property
    def total_duration(self) -> float:
        if not self.scenes:
            return 0.0
        last = self.scenes[-1]
        return last.start_time + last.duration

    def scene_at(self, t: float) -> SceneSpec | None:
        """Return the scene active at global time t, or None."""
        for scene in self.scenes:
            if scene.start_time <= t < scene.end_time:
                return scene
        # Handle the last frame edge case
        if self.scenes and t >= self.scenes[-1].start_time:
            return self.scenes[-1]
        return None

    def audio_timings(self) -> list[tuple[str, float]]:
        """
        Return (audio_path, start_time_seconds) for all sample scenes.
        Used by FFmpeg to mix audio at correct timestamps.
        """
        timings: list[tuple[str, float]] = []
        for scene in self.scenes:
            if scene.scene_type == "sample" and "audio_path" in scene.data:
                timings.append((scene.data["audio_path"], scene.start_time))
        return timings
