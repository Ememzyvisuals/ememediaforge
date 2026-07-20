"""EmemediaForge audio — analysis, waveform, duration."""

from ememediaforge.audio.analyzer import (
    compute_rms,
    find_voiced_segments,
    get_duration,
    get_waveform_frames,
    load_audio,
)
from ememediaforge.audio.duration import format_duration, get_audio_duration
from ememediaforge.audio.waveform import extract_amplitude_envelope

__all__ = [
    "load_audio",
    "get_duration",
    "compute_rms",
    "find_voiced_segments",
    "get_waveform_frames",
    "get_audio_duration",
    "format_duration",
    "extract_amplitude_envelope",
]
