"""EmemediaForge — Dark theme: near-black canvas, neon green accent.
Perfect for NaijaVox, Africlaude, and AI model demos.
"""

from ememediaforge.themes.base import Theme

DARK_THEME = Theme(
    name="dark",
    bg_color=(8, 8, 12),
    surface_color=(18, 18, 28),
    accent_color=(0, 255, 136),
    accent_dim=(0, 180, 90),
    text_primary=(255, 255, 255),
    text_secondary=(160, 160, 170),
    word_active=(0, 255, 136),
    word_past=(80, 80, 100),
    word_future=(45, 45, 60),
    waveform_color=(0, 255, 136),
    progress_color=(0, 200, 100),
    overlay_color=(8, 8, 12, 200),
)
