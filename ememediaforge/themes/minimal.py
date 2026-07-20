"""EmemediaForge — Minimal theme: off-white canvas, pure black accent."""

from ememediaforge.themes.base import Theme

MINIMAL_THEME = Theme(
    name="minimal",
    bg_color=(250, 250, 250),
    surface_color=(240, 240, 240),
    accent_color=(0, 0, 0),
    accent_dim=(50, 50, 50),
    text_primary=(0, 0, 0),
    text_secondary=(100, 100, 100),
    word_active=(0, 0, 0),
    word_past=(180, 180, 180),
    word_future=(210, 210, 210),
    waveform_color=(0, 0, 0),
    progress_color=(80, 80, 80),
    overlay_color=(250, 250, 250, 200),
)
