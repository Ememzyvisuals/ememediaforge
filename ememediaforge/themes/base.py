"""
EmemediaForge — Base Theme dataclass.
Themes define visual appearance without affecting rendering logic.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Theme:
    """
    Immutable visual theme. All colors are (R, G, B) tuples 0-255.

    Attributes
    ----------
    name            : Theme identifier string
    bg_color        : Canvas background color
    surface_color   : Card / panel background color
    accent_color    : Primary accent (active word, waveform, highlights)
    accent_dim      : Dimmer version of accent for past words
    text_primary    : Main text color (title, active transcript)
    text_secondary  : Secondary text color (voice label, subtitles)
    word_active     : Active/current karaoke word color
    word_past       : Already-spoken word color
    word_future     : Not-yet-spoken word color
    waveform_color  : Waveform bar color
    progress_color  : Progress bar / indicator color
    overlay_color   : Semi-transparent overlay color (R, G, B, A)
    """

    name: str
    bg_color: tuple[int, int, int]
    surface_color: tuple[int, int, int]
    accent_color: tuple[int, int, int]
    accent_dim: tuple[int, int, int]
    text_primary: tuple[int, int, int]
    text_secondary: tuple[int, int, int]
    word_active: tuple[int, int, int]
    word_past: tuple[int, int, int]
    word_future: tuple[int, int, int]
    waveform_color: tuple[int, int, int]
    progress_color: tuple[int, int, int]
    overlay_color: tuple[int, int, int, int]


# ── Registry ──────────────────────────────────────────────────────────────────


def get_theme(name: str) -> Theme:
    """
    Return a Theme by name.

    Available themes
    ----------------
    modern   White bg, purple accent   — professional, HuggingFace-style
    light    White bg, blue accent     — clean, academic, LinkedIn-ready
    dark     Near-black, neon green    — tech/AI demos, NaijaVox/Africlaude
    minimal  Off-white, black accent   — typographic, minimal distraction

    Raises ValueError for unknown theme names.
    """
    from ememediaforge.themes.dark import DARK_THEME
    from ememediaforge.themes.light import LIGHT_THEME
    from ememediaforge.themes.minimal import MINIMAL_THEME
    from ememediaforge.themes.modern import MODERN_THEME

    registry: dict[str, Theme] = {
        "modern": MODERN_THEME,
        "light": LIGHT_THEME,
        "dark": DARK_THEME,
        "minimal": MINIMAL_THEME,
    }
    key = name.lower().strip()
    if key not in registry:
        raise ValueError(f"Unknown theme '{key}'. Available: {', '.join(sorted(registry))}")
    return registry[key]


def list_themes() -> list[str]:
    """Return all available theme names."""
    return ["modern", "light", "dark", "minimal"]
