"""
EmemediaForge — Sample Scene: the main showcase frame.

Renders per-frame:
  ┌──────────────────────────────────────────────────┐
  │  [Logo]   [Model Name]         [Voice Label]     │  Header
  ├──────────────────────────────────────────────────┤
  │                                                  │
  │            Karaoke Transcript                    │  Body
  │     (active word highlighted in accent color)    │
  │                                                  │
  ├──────────────────────────────────────────────────┤
  │   [Sample N/M]   ──────────────────────────────  │  Progress
  ├──────────────────────────────────────────────────┤
  │        ████ ██ ████ █ ███ ████ ██ █████ ██       │  Waveform
  └──────────────────────────────────────────────────┘
"""
from __future__ import annotations

import math
from PIL import Image, ImageDraw

from ememediaforge.scenes.base import BaseScene, ease_in_out, clip
from ememediaforge.assets.loader import FontManager
from ememediaforge.alignment.timestamps import WordTimestamp
from ememediaforge.themes.base import Theme


class SampleScene(BaseScene):
    """
    Main showcase scene. Displays:
    - Model name header
    - Voice/sample label
    - Karaoke transcript with word-level highlight
    - Animated waveform bars
    - Progress bar
    """

    def __init__(
        self,
        theme: Theme,
        width: int,
        height: int,
        fps: int,
        model_name: str,
        voice_label: str,
        words: list[WordTimestamp],
        waveform_frames: list[list[float]],   # pre-computed per video-frame
        audio_duration: float,
        sample_index: int,
        total_samples: int,
        logo: str | None = None,
        template: str = "tts",
    ):
        super().__init__(theme, width, height, fps)
        self.model_name     = model_name
        self.voice_label    = voice_label
        self.words          = words
        self.waveform_frames = waveform_frames
        self.audio_duration  = audio_duration
        self.sample_index    = sample_index
        self.total_samples   = total_samples
        self.logo            = logo
        self.template        = template

        # Layout zones (relative to height)
        self._header_h   = int(height * 0.14)
        self._footer_h   = int(height * 0.28)
        self._body_y1    = self._header_h
        self._body_y2    = height - self._footer_h
        self._wave_y1    = height - self._footer_h + int(height * 0.06)
        self._wave_y2    = height - int(height * 0.04)
        self._prog_y     = height - self._footer_h + int(height * 0.02)

    def render(self, local_t: float) -> Image.Image:
        img  = self.blank()
        draw = ImageDraw.Draw(img)

        # Fade in first 0.3 sec
        alpha = clip(ease_in_out(local_t / 0.3), 0.0, 1.0)

        self._draw_header(img, draw, alpha)
        self._draw_body(draw, local_t, alpha)
        self._draw_progress(draw, local_t, alpha)
        self._draw_waveform(draw, local_t)

        return self.fade_image(img, alpha)

    # ── Header ───────────────────────────────────────────────────────────────

    def _draw_header(self, img: Image.Image, draw: ImageDraw.ImageDraw,
                     alpha: float) -> None:
        pad   = int(self.width * 0.04)
        cx    = self.width // 2
        mid_y = self._header_h // 2

        # Thin accent line at very top
        line_h = max(2, int(self.height * 0.004))
        line_w = int(self.width * alpha)
        draw.rectangle([0, 0, line_w, line_h], fill=self.theme.accent_color)

        # Logo (left-aligned)
        logo_size = int(min(self._header_h - 12, 52))
        logo_x = pad + logo_size // 2
        logo_y = mid_y
        if self.logo:
            self.draw_logo(img, self.logo, logo_x, logo_y, size=logo_size)
            text_x_start = logo_x + logo_size // 2 + int(self.width * 0.02)
        else:
            text_x_start = pad

        # Model name
        name_size = max(10, int(self._header_h * 0.42))
        f_name    = FontManager.get_font(name_size, "bold")
        name_color = tuple(int(c * alpha) for c in self.theme.text_primary)
        name_y = mid_y - name_size // 2 - 2
        draw.text((text_x_start, name_y), self.model_name, font=f_name, fill=name_color)

        # Voice label (right-aligned, accent colored badge)
        label_size = max(9, int(self._header_h * 0.28))
        f_label   = FontManager.get_font(label_size, "regular")
        label_color = tuple(int(c * alpha) for c in self.theme.accent_color)
        lb = draw.textbbox((0, 0), self.voice_label, font=f_label)
        lw = lb[2] - lb[0]
        label_x = self.width - pad - lw
        label_y = mid_y - label_size // 2

        # Badge background
        badge_pad = int(label_size * 0.4)
        badge_r, badge_g, badge_b = self.theme.accent_color
        badge_alpha = int(30 * alpha)
        badge_fill = (badge_r // 6, badge_g // 6, badge_b // 6)
        draw.rounded_rectangle(
            [label_x - badge_pad, label_y - badge_pad // 2,
             label_x + lw + badge_pad, label_y + label_size + badge_pad // 2],
            radius=label_size // 3, fill=badge_fill,
            outline=self.theme.accent_color,
        )
        draw.text((label_x, label_y), self.voice_label, font=f_label, fill=label_color)

        # Horizontal separator
        sep_y  = self._header_h - 1
        sep_color = tuple(max(0, c - 30) for c in self.theme.bg_color) \
            if self.theme.bg_color[0] > 128 \
            else tuple(min(255, c + 25) for c in self.theme.bg_color)
        draw.line([(pad, sep_y), (self.width - pad, sep_y)],
                  fill=sep_color, width=1)

    # ── Body: karaoke transcript ──────────────────────────────────────────────

    def _draw_body(self, draw: ImageDraw.ImageDraw, local_t: float,
                   alpha: float) -> None:
        if not self.words:
            # No transcript: show waiting dots
            self._draw_placeholder(draw, local_t, alpha)
            return

        font_size = max(14, int((self._body_y2 - self._body_y1) * 0.155))
        rect = (
            int(self.width * 0.05),
            self._body_y1,
            int(self.width * 0.95),
            self._body_y2,
        )
        self.draw_karaoke(draw, self.words, local_t, rect, font_size=font_size)

    def _draw_placeholder(self, draw: ImageDraw.ImageDraw, local_t: float,
                          alpha: float) -> None:
        """Animated dots when no transcript is available."""
        dots = "●" * (int(local_t * 2) % 4)
        f = FontManager.get_font(int(self.height * 0.06), "regular")
        c = tuple(int(c * alpha) for c in self.theme.text_secondary)
        cy = (self._body_y1 + self._body_y2) // 2
        self.draw_text_centered(draw, dots or "●", cy, f, c)

    # ── Progress bar ─────────────────────────────────────────────────────────

    def _draw_progress(self, draw: ImageDraw.ImageDraw, local_t: float,
                       alpha: float) -> None:
        pad  = int(self.width * 0.06)
        y    = self._prog_y
        bar_h = max(2, int(self.height * 0.006))
        total_w = self.width - 2 * pad

        # Track background
        track_color = tuple(max(0, c - 20) if c > 128 else min(255, c + 20)
                            for c in self.theme.bg_color)
        draw.rectangle([pad, y, pad + total_w, y + bar_h], fill=track_color)

        # Fill (clamped to audio_duration)
        fill_ratio = clip(local_t / max(0.01, self.audio_duration), 0.0, 1.0)
        fill_w = int(total_w * fill_ratio * alpha)
        if fill_w > 0:
            draw.rectangle([pad, y, pad + fill_w, y + bar_h],
                           fill=self.theme.progress_color)

        # Sample counter e.g. "2 / 3"
        counter = f"{self.sample_index + 1} / {self.total_samples}"
        f_counter = FontManager.get_font(max(8, int(self.height * 0.022)), "regular")
        counter_color = tuple(int(c * alpha * 0.6) for c in self.theme.text_secondary)
        cb = draw.textbbox((0, 0), counter, font=f_counter)
        cw = cb[2] - cb[0]
        draw.text((self.width - pad - cw, y - int(self.height * 0.022)),
                  counter, font=f_counter, fill=counter_color)

    # ── Waveform ─────────────────────────────────────────────────────────────

    def _draw_waveform(self, draw: ImageDraw.ImageDraw, local_t: float) -> None:
        frame_idx = min(
            int(local_t * self.fps),
            len(self.waveform_frames) - 1
        )
        if frame_idx < 0 or not self.waveform_frames:
            return

        amplitudes = self.waveform_frames[frame_idx]
        pad  = int(self.width * 0.06)
        rect = (pad, self._wave_y1, self.width - pad, self._wave_y2)
        self.draw_waveform_bars(draw, amplitudes, rect)
