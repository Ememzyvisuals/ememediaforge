"""
EmemediaForge — Intro scene: animated fade-in with logo + model title.
"""

from __future__ import annotations

from PIL import Image, ImageDraw

from ememediaforge.assets.loader import FontManager
from ememediaforge.scenes.base import BaseScene, clip, ease_in_out
from ememediaforge.themes.base import Theme


class IntroScene(BaseScene):
    """
    Fade-in intro scene showing:
      - Background fill
      - Logo (if provided) fading in
      - Model name (large grotesk bold)
      - Description subtitle
      - Subtle tagline
    """

    def __init__(
        self,
        theme: Theme,
        width: int,
        height: int,
        fps: int,
        title: str,
        description: str = "",
        author: str = "",
        url: str = "",
        logo: str | None = None,
        duration: float = 1.8,
    ):
        super().__init__(theme, width, height, fps)
        self.title = title
        self.description = description
        self.author = author
        self.url = url
        self.logo = logo
        self.duration = duration

    def render(self, local_t: float) -> Image.Image:
        progress = ease_in_out(clip(local_t / self.duration, 0.0, 1.0))
        img = self.blank()
        draw = ImageDraw.Draw(img)

        cx = self.width // 2
        cy = self.height // 2

        # ── Subtle background grid / accent lines ──────────────────────────
        self._draw_accent_lines(draw, progress)

        # ── Logo ───────────────────────────────────────────────────────────
        logo_bottom = cy - int(self.height * 0.18)
        if self.logo:
            logo_size = int(88 * progress)
            if logo_size > 4:
                self.draw_logo(img, self.logo, cx, logo_bottom, size=logo_size)

        # ── Model Name ─────────────────────────────────────────────────────
        title_size = max(12, int(self.height * 0.072))
        f_title = FontManager.get_font(title_size, "bold")
        alpha_color = tuple(int(c * progress) for c in self.theme.text_primary)
        title_y = cy - int(title_size * 0.5)
        if self.logo:
            title_y = logo_bottom + int(self.height * 0.06)
        self.draw_text_centered(draw, self.title, title_y, f_title, alpha_color)

        # ── Description ────────────────────────────────────────────────────
        if self.description:
            desc_size = max(10, int(self.height * 0.033))
            f_desc = FontManager.get_font(desc_size, "regular")
            desc_color = tuple(int(c * progress) for c in self.theme.text_secondary)
            desc_y = title_y + title_size + int(self.height * 0.025)
            self.draw_text_centered(draw, self.description, desc_y, f_desc, desc_color)

        # ── Accent underline beneath title ─────────────────────────────────
        underline_w = int(self.width * 0.12 * progress)
        underline_h = max(2, int(self.height * 0.005))
        ux1 = cx - underline_w // 2
        ux2 = cx + underline_w // 2
        uy = title_y + title_size + int(self.height * 0.008)
        if self.description:
            # Place underline right below title, above description
            uy = title_y + title_size + int(self.height * 0.008)
        draw.rectangle([ux1, uy, ux2, uy + underline_h], fill=self.theme.accent_color)

        # ── Author / URL footer ────────────────────────────────────────────
        if self.author or self.url:
            footer = self.author or self.url
            f_footer = FontManager.get_font(max(9, int(self.height * 0.022)), "regular")
            footer_color = tuple(int(c * progress * 0.6) for c in self.theme.text_secondary)
            footer_y = self.height - int(self.height * 0.1)
            self.draw_text_centered(draw, footer, footer_y, f_footer, footer_color)

        return self.fade_image(img, progress)

    def _draw_accent_lines(self, draw: ImageDraw.ImageDraw, progress: float) -> None:
        """Subtle decorative corner accent lines."""
        r, g, b = self.theme.accent_color
        c = (max(0, r - 60), max(0, g - 60), max(0, b - 60))
        # Top-left
        draw.line([(0, 0), (int(self.width * 0.15), 0)], fill=c, width=2)
        draw.line([(0, 0), (0, int(self.height * 0.08))], fill=c, width=2)
        # Bottom-right
        draw.line(
            [(self.width, self.height), (self.width - int(self.width * 0.15), self.height)],
            fill=c,
            width=2,
        )
        draw.line(
            [(self.width, self.height), (self.width, self.height - int(self.height * 0.08))],
            fill=c,
            width=2,
        )
