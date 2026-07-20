"""
EmemediaForge — Waveform utilities.
High-level helpers for waveform data extraction.
"""
from __future__ import annotations
import numpy as np
from pathlib import Path
from ememediaforge.audio.analyzer import load_audio, compute_rms


def extract_amplitude_envelope(path: Path | str, fps: int = 30,
                                n_bars: int = 64, sr: int = 22050
                                ) -> tuple[list[list[float]], float]:
    """
    Extract per-frame waveform bar amplitudes from an audio file.

    Returns
    -------
    (frames, duration)
    frames   : list of per-frame amplitude lists [0.0–1.0]
    duration : audio duration in seconds
    """
    y, sr = load_audio(path, sr=sr)
    duration = len(y) / sr
    total_frames = int(duration * fps) + 1
    window = int(sr * 0.8)

    result: list[list[float]] = []
    for fi in range(total_frames):
        center = int((fi / fps) * sr)
        seg = y[max(0, center - window//2): min(len(y), center + window//2)]
        if len(seg) < n_bars:
            seg = np.pad(seg, (0, max(0, n_bars - len(seg))))
        chunk = max(1, len(seg) // n_bars)
        amps = [float(np.abs(seg[i*chunk:(i+1)*chunk]).mean()) for i in range(n_bars)]
        peak = max(amps) if max(amps) > 1e-6 else 1.0
        result.append([a / peak for a in amps])

    return result, duration
