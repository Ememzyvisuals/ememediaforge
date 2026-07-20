"""
EmemediaForge — Abstract base scene + shared drawing utilities.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from PIL import Image, ImageDraw

from ememediaforge.assets.loader import FontManager, load_logo
from ememediaforge.themes.base import Theme


class BaseScene(ABC):
    """Abstract scene. Every scene must implement render()."""

    def __init__(self, theme: Theme, width: int, height: int, fps: int = 30):
        self.theme = theme
        self.width = width
        self.height = height
        self.fps = fps

    @abstractmethod
    def render(self, local_t: float) -> Image.Image:
        """
        Render a single frame at local time `local_t` (seconds from scene start).
        Must return a PIL Image in RGB mode.
        """
        ...

    # ── Shared helpers ────────────────────────────────────────────────────────

    def blank(self, color: tuple | None = None) -> Image.Image:
        """Create a blank canvas filled with the theme background color."""
        c = color or self.theme.bg_color
        return Image.new("RGB", (self.width, self.height), color=c)

    def draw_text_centered(
        self,
        draw: ImageDraw.ImageDraw,
        text: str,
        y: int,
        font,
        color: tuple,
        x_override: int | None = None,
    ) -> tuple[int, int]:
        """Draw text centered horizontally. Returns (x, y) of drawn text."""
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        x = x_override if x_override is not None else (self.width - w) // 2
        draw.text((x, y), text, font=font, fill=color)
        return x, y

    def draw_logo(
        self,
        img: Image.Image,
        logo_path: str | None,
        cx: int,
        cy: int,
        size: int = 72,
    ) -> int:
        """Paste logo centered at (cx, cy). Returns the bottom y after logo."""
        if not logo_path:
            return cy
        logo = load_logo(Path(logo_path), size=(size, size))
        if logo is None:
            return cy
        lx = cx - logo.width // 2
        ly = cy - logo.height // 2
        if logo.mode == "RGBA":
            img.paste(logo, (lx, ly), logo)
        else:
            img.paste(logo, (lx, ly))
        return ly + logo.height

    def draw_waveform_bars(
        self,
        draw: ImageDraw.ImageDraw,
        amplitudes: list[float],
        rect: tuple[int, int, int, int],
    ) -> None:
        """
        Draw animated mirrored waveform bars (music-visualizer style).

        Parameters
        ----------
        amplitudes : list of n_bars floats 0.0-1.0
        rect       : (x1, y1, x2, y2) bounding box for the waveform
        """
        x1, y1, x2, y2 = rect
        n = len(amplitudes)
        if n == 0:
            return

        total_w = x2 - x1
        slot_w = total_w / n
        bar_w = max(2, int(slot_w * 0.65))
        center_y = (y1 + y2) // 2
        max_h = ((y2 - y1) // 2) - 2
        min_h = 3
        gap = max(0, (slot_w - bar_w) // 2)

        for i, amp in enumerate(amplitudes):
            bar_h = max(min_h, int(amp * max_h))
            bx1 = int(x1 + i * slot_w + gap)
            bx2 = bx1 + bar_w

            # Glow: draw a slightly wider, dimmer bar behind
            r, g, b = self.theme.waveform_color
            glow_color = (r // 4, g // 4, b // 4)
            draw.rectangle(
                [bx1 - 1, center_y - bar_h - 2, bx2 + 1, center_y + bar_h + 2], fill=glow_color
            )

            # Main bar
            draw.rectangle(
                [bx1, center_y - bar_h, bx2, center_y + bar_h], fill=self.theme.waveform_color
            )

    def draw_karaoke(
        self,
        draw: ImageDraw.ImageDraw,
        words: list,  # list[WordTimestamp]
        local_t: float,
        rect: tuple[int, int, int, int],
        font_size: int = 36,
    ) -> None:
        """
        Render karaoke-style word highlighting inside rect.
        Active word = accent color + bold.
        Past = dim. Future = muted.
        Shows a sliding window of ~3 lines.
        """
        if not words:
            return

        x1, y1, x2, y2 = rect
        max_w = x2 - x1 - 60
        f_reg = FontManager.get_font(font_size, "regular")
        f_bold = FontManager.get_font(font_size, "bold")

        # Build lines (word-wrap)
        lines: list[list[tuple[int, str]]] = []  # [(word_idx, word), ...]
        line: list[tuple[int, str]] = []
        line_px = 0
        space_w = draw.textbbox((0, 0), " ", font=f_reg)[2]

        for idx, wt in enumerate(words):
            w_bbox = draw.textbbox((0, 0), wt.word, font=f_bold)
            w_px = w_bbox[2] - w_bbox[0]
            if line and line_px + space_w + w_px > max_w:
                lines.append(line)
                line = [(idx, wt.word)]
                line_px = w_px
            else:
                line.append((idx, wt.word))
                line_px = line_px + space_w + w_px if line_px else w_px

        if line:
            lines.append(line)

        # Find active word + line
        active_idx = -1
        for i, wt in enumerate(words):
            if wt.start <= local_t < wt.end:
                active_idx = i
                break
        if active_idx == -1 and local_t >= words[-1].end:
            active_idx = len(words) - 1

        active_line = 0
        for li, ln in enumerate(lines):
            if any(wi == active_idx for wi, _ in ln):
                active_line = li
                break

        # Sliding window: show 3 lines around active
        start_ln = max(0, active_line - 1)
        visible = lines[start_ln : start_ln + 3]

        line_h = int(font_size * 1.65)
        total_h = len(visible) * line_h
        start_y = (y1 + y2) // 2 - total_h // 2

        for li, ln in enumerate(visible):
            # Measure line to center it
            words_in_line = [w for _, w in ln]
            line_str = " ".join(words_in_line)
            lb = draw.textbbox((0, 0), line_str, font=f_bold)
            line_px_w = lb[2] - lb[0]
            cx = (x1 + x2) // 2
            x = cx - line_px_w // 2
            y = start_y + li * line_h

            for wi, word in ln:
                wt = words[wi]
                is_active = wi == active_idx
                is_past = local_t >= wt.end
                font = f_bold if is_active else f_reg
                if is_active:
                    color = self.theme.word_active
                elif is_past:
                    color = self.theme.word_past
                else:
                    color = self.theme.word_future

                draw.text((x, y), word, font=font, fill=color)
                wb = draw.textbbox((x, y), word, font=font)
                x += (wb[2] - wb[0]) + space_w

    def fade_image(self, img: Image.Image, alpha: float) -> Image.Image:
        """Blend img toward background color by factor (0=full, 1=original)."""
        bg = self.blank()
        return Image.blend(bg, img, clip(alpha, 0.0, 1.0))


def clip(val, lo, hi):
    return max(lo, min(hi, val))


def ease_in_out(t: float) -> float:
    """Smooth cubic easing 0→1."""
    return 3 * t**2 - 2 * t**3
