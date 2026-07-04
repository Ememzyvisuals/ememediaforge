"""
EmemediaForge — Transition scene: fast dip-to-black between samples.
"""
from __future__ import annotations
from PIL import Image
from ememediaforge.scenes.base import BaseScene, ease_in_out, clip
from ememediaforge.themes.base import Theme


class TransitionScene(BaseScene):
    def __init__(self, theme: Theme, width: int, height: int, fps: int,
                 duration: float = 0.45):
        super().__init__(theme, width, height, fps)
        self.duration = duration

    def render(self, local_t: float) -> Image.Image:
        # Dip to black at midpoint
        progress = local_t / self.duration
        if progress < 0.5:
            alpha = 1.0 - ease_in_out(progress / 0.5)  # fade out
        else:
            alpha = ease_in_out((progress - 0.5) / 0.5)  # fade in
        bg = self.blank()
        black = Image.new("RGB", (self.width, self.height), (0, 0, 0))
        return Image.blend(black, bg, clip(alpha, 0.0, 1.0))
