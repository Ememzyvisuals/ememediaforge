"""
EmemediaForge — STT (Speech-to-Text) template descriptor.

Layout:
  - Logo + Model Name header
  - Transcript reveal (words appear progressively as audio plays)
  - Animated waveform bars
  - Audio progress bar + Sample counter

Used when: you have an ASR/STT model and want to show speech → text transcription.
The transcript is what the model PREDICTED from the audio input.
"""
from __future__ import annotations

TEMPLATE_ID = "stt"

DESCRIPTION = (
    "Speech-to-Text showcase: transcript words reveal progressively as audio plays."
)

INTRO_DURATION  = 1.8
OUTRO_DURATION  = 2.0
SAMPLE_PADDING  = 0.40
TRANSITION_DUR  = 0.45

def get_config() -> dict:
    return {
        "id":               TEMPLATE_ID,
        "description":      DESCRIPTION,
        "intro_duration":   INTRO_DURATION,
        "outro_duration":   OUTRO_DURATION,
        "sample_padding":   SAMPLE_PADDING,
        "transition_dur":   TRANSITION_DUR,
        "show_karaoke":     True,
        "show_waveform":    True,
        "show_progress":    True,
        "karaoke_mode":     "reveal",
    }
