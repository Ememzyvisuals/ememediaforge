"""
EmemediaForge — Outro scene: fade-out with branding + call-to-action.
"""
from __future__ import annotations
from PIL import Image, ImageDraw
from ememediaforge.scenes.base import BaseScene, ease_in_out, clip
from ememediaforge.assets.loader import FontManager
from ememediaforge.themes.base import Theme


class OutroScene(BaseScene):
    def __init__(self, theme: Theme, width: int, height: int, fps: int,
                 title: str, url: str = "", logo: str | None = None,
                 duration: float = 2.0):
        super().__init__(theme, width, height, fps)
        self.title    = title
        self.url      = url
        self.logo     = logo
        self.duration = duration

    def render(self, local_t: float) -> Image.Image:
        # Fade in then fade out
        half = self.duration / 2
        if local_t < half:
            alpha = ease_in_out(local_t / half)
        else:
            alpha = ease_in_out(1.0 - (local_t - half) / half)

        img  = self.blank()
        draw = ImageDraw.Draw(img)
        cx   = self.width  // 2
        cy   = self.height // 2

        # ── Accent circle ──────────────────────────────────────────────────
        r, g, b = self.theme.accent_color
        glow = (r // 8, g // 8, b // 8)
        radius = int(self.width * 0.22)
        draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
                     fill=glow)

        # ── Logo ───────────────────────────────────────────────────────────
        if self.logo:
            self.draw_logo(img, self.logo, cx, cy - int(self.height * 0.12), size=72)

        # ── Title ──────────────────────────────────────────────────────────
        title_size = max(12, int(self.height * 0.062))
        f_title = FontManager.get_font(title_size, "bold")
        title_color = tuple(int(c * alpha) for c in self.theme.text_primary)
        self.draw_text_centered(draw, self.title,
                                cy - title_size // 2, f_title, title_color)

        # ── URL ────────────────────────────────────────────────────────────
        if self.url:
            url_size = max(9, int(self.height * 0.028))
            f_url = FontManager.get_font(url_size, "regular")
            url_color = tuple(int(c * alpha) for c in self.theme.accent_color)
            self.draw_text_centered(draw, self.url,
                                    cy + title_size + int(self.height * 0.03),
                                    f_url, url_color)

        # ── EmemediaForge watermark ────────────────────────────────────────
        wm_size = max(8, int(self.height * 0.022))
        f_wm    = FontManager.get_font(wm_size, "regular")
        wm_color = tuple(int(c * alpha * 0.45) for c in self.theme.text_secondary)
        self.draw_text_centered(draw, "Made with EmemediaForge by @Ememzyvisuals",
                                self.height - int(self.height * 0.09),
                                f_wm, wm_color)

        return self.fade_image(img, alpha)
