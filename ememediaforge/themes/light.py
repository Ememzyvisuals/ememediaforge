"""
EmemediaForge — Light theme: crisp white canvas with electric blue accent.

Perfect for:
  - Academic paper demos
  - Professional LinkedIn posts
  - HuggingFace model cards (matches their white UI)
  - Light-mode screenshots

Visual identity:
  bg      #FFFFFF  clean white
  surface #F0F4FF  blue-tinted white card
  accent  #2563EB  electric blue
  text    #0F172A  near-black (Slate 900)
"""

from ememediaforge.themes.base import Theme

LIGHT_THEME = Theme(
    name="light",
    bg_color=(255, 255, 255),  # Pure white
    surface_color=(240, 244, 255),  # Blue-tinted card
    accent_color=(37, 99, 235),  # Electric blue #2563EB
    accent_dim=(147, 197, 253),  # Light blue #93C5FD
    text_primary=(15, 23, 42),  # Slate-900 near-black
    text_secondary=(100, 116, 139),  # Slate-500
    word_active=(37, 99, 235),  # Electric blue — active word
    word_past=(148, 163, 184),  # Slate-400 — spoken words
    word_future=(203, 213, 225),  # Slate-300 — upcoming words
    waveform_color=(37, 99, 235),  # Blue waveform bars
    progress_color=(96, 165, 250),  # Blue-400 progress
    overlay_color=(255, 255, 255, 210),  # White overlay for fades
)
