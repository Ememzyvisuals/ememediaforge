"""
EmemediaForge — Audio analysis using librosa.
Handles loading, RMS energy, and voiced segment detection.
"""
from __future__ import annotations
import numpy as np
import librosa
from pathlib import Path
from ememediaforge.core.exceptions import AudioProcessingError


def load_audio(path: Path | str, sr: int = 22050, mono: bool = True):
    """Load audio file. Returns (y: ndarray, sr: int)."""
    try:
        y, sr_out = librosa.load(str(path), sr=sr, mono=mono)
        return y, sr_out
    except Exception as e:
        raise AudioProcessingError(f"Failed to load audio {path}: {e}") from e


def get_duration(path: Path | str) -> float:
    """Return audio duration in seconds without decoding the full file."""
    try:
        return librosa.get_duration(path=str(path))
    except Exception as e:
        raise AudioProcessingError(f"Cannot read duration of {path}: {e}") from e


def compute_rms(y: np.ndarray, frame_length: int = 2048,
                hop_length: int = 512) -> np.ndarray:
    """Compute per-frame RMS energy envelope."""
    return librosa.feature.rms(y=y, frame_length=frame_length,
                                hop_length=hop_length)[0]


def find_voiced_segments(rms: np.ndarray, sr: int,
                         hop_length: int = 512,
                         threshold_factor: float = 0.12
                         ) -> list[tuple[float, float]]:
    """
    Detect contiguous voiced (non-silent) segments.
    Returns list of (start_seconds, end_seconds) tuples.
    """
    if rms.max() < 1e-6:
        return []
    threshold = rms.max() * threshold_factor
    voiced = rms > threshold

    segments: list[tuple[float, float]] = []
    in_seg = False
    start_frame = 0

    for i, v in enumerate(voiced):
        if v and not in_seg:
            in_seg = True
            start_frame = i
        elif not v and in_seg:
            in_seg = False
            t_start = librosa.frames_to_time(start_frame, sr=sr, hop_length=hop_length)
            t_end   = librosa.frames_to_time(i, sr=sr, hop_length=hop_length)
            segments.append((float(t_start), float(t_end)))

    if in_seg:
        t_start = librosa.frames_to_time(start_frame, sr=sr, hop_length=hop_length)
        t_end   = librosa.frames_to_time(len(voiced) - 1, sr=sr, hop_length=hop_length)
        segments.append((float(t_start), float(t_end)))

    # Merge segments that are < 100 ms apart
    merged: list[tuple[float, float]] = []
    for seg in segments:
        if merged and seg[0] - merged[-1][1] < 0.1:
            merged[-1] = (merged[-1][0], seg[1])
        else:
            merged.append(seg)

    return merged


def get_waveform_frames(y: np.ndarray, sr: int,
                        total_video_frames: int,
                        n_bars: int = 64,
                        fps: int = 30) -> list[list[float]]:
    """
    Pre-compute waveform bar amplitudes for every video frame.
    Returns a list[list[float]] of shape [total_video_frames, n_bars].
    Each inner list is n_bars amplitude values 0.0-1.0.
    """
    result: list[list[float]] = []
    audio_len = len(y)
    window_samples = int(sr * 0.8)  # 800 ms rolling window

    for frame_idx in range(total_video_frames):
        center = int((frame_idx / fps) * sr)
        start = max(0, center - window_samples // 2)
        end   = min(audio_len, center + window_samples // 2)
        seg   = y[start:end]

        if len(seg) < n_bars:
            seg = np.pad(seg, (0, max(0, n_bars - len(seg))))

        chunk = max(1, len(seg) // n_bars)
        amps = [float(np.abs(seg[i*chunk:(i+1)*chunk]).mean())
                for i in range(n_bars)]
        peak = max(amps) if max(amps) > 1e-6 else 1.0
        result.append([a / peak for a in amps])

    return result
