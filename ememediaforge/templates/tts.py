"""
EmemediaForge — TTS (Text-to-Speech) template descriptor.

Layout:
  - Logo + Model Name header
  - Karaoke transcript (words highlight as spoken)
  - Animated waveform bars (bottom)
  - Progress bar + Sample counter

Used when: you have a TTS model and want to show text → speech conversion.
The transcript is what the model was GIVEN as input text.
"""

from __future__ import annotations

TEMPLATE_ID = "tts"

DESCRIPTION = "Text-to-Speech showcase: words highlight in sync with the synthesized audio."

# Scene durations (seconds)
INTRO_DURATION = 1.8
OUTRO_DURATION = 2.0
SAMPLE_PADDING = 0.40
TRANSITION_DUR = 0.45

# Layout ratios (fraction of total height)
HEADER_RATIO = 0.14
FOOTER_RATIO = 0.28  # waveform + progress
BODY_RATIO = 1.0 - HEADER_RATIO - FOOTER_RATIO

# Font sizes (fraction of height)
TITLE_SIZE_RATIO = 0.072
SUBTITLE_SIZE_RATIO = 0.033
LABEL_SIZE_RATIO = 0.028
BODY_FONT_RATIO = 0.055


def get_config() -> dict:
    """Return default template configuration."""
    return {
        "id": TEMPLATE_ID,
        "description": DESCRIPTION,
        "intro_duration": INTRO_DURATION,
        "outro_duration": OUTRO_DURATION,
        "sample_padding": SAMPLE_PADDING,
        "transition_dur": TRANSITION_DUR,
        "show_karaoke": True,
        "show_waveform": True,
        "show_progress": True,
        "karaoke_mode": "highlight",  # highlight | reveal | both
    }
