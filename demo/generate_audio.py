"""
EmemediaForge — Synthetic audio generator for CI demo builds.

Generates speech-like WAV files that produce realistic waveform
visualizations without requiring real voice recordings.

Usage:
    python demo/generate_audio.py
"""
import sys
from pathlib import Path

import numpy as np
import soundfile as sf


def generate_speech_like(
    duration: float = 3.5,
    sr: int = 22050,
    pitch: float = 150.0,
    seed: int = 42,
) -> np.ndarray:
    """
    Generate audio that resembles natural speech in its energy envelope.

    Uses harmonic synthesis + syllable-burst amplitude modulation
    to produce waveforms that animate naturally in the waveform visualizer.
    """
    np.random.seed(seed)
    t = np.linspace(0, duration, int(sr * duration), dtype=np.float32)

    # Harmonic stack (fundamental + overtones) — sounds voice-like
    signal = np.zeros_like(t)
    for k in range(1, 10):
        # Each harmonic slightly detuned for natural warmth
        freq = pitch * k * (1 + np.random.uniform(-0.002, 0.002))
        signal += (1.0 / k) * np.sin(2 * np.pi * freq * t)

    # Syllable bursts: ~3.5 per second (natural speech rate)
    syllables_per_sec = 3.5
    n_syllables = max(1, int(duration * syllables_per_sec))
    envelope = np.zeros_like(t)

    for i in range(n_syllables):
        # Slight jitter on syllable timing
        jitter = np.random.uniform(-0.04, 0.04)
        center = (i + 0.5 + jitter) * duration / n_syllables
        width = np.random.uniform(0.006, 0.012)
        amp = np.random.uniform(0.6, 1.0)
        envelope += amp * np.exp(-((t - center) ** 2) / width)

    # Soft noise floor (breath, room tone)
    noise = np.random.randn(len(t)).astype(np.float32) * 0.015

    signal = signal * np.clip(envelope, 0, 1) * 0.35 + noise
    signal = np.clip(signal, -1.0, 1.0)

    # Brief silence at start and end (natural padding)
    fade = int(sr * 0.08)
    signal[:fade] *= np.linspace(0, 1, fade)
    signal[-fade:] *= np.linspace(1, 0, fade)

    return signal


def main() -> None:
    samples_dir = Path(__file__).parent / "samples"
    samples_dir.mkdir(parents=True, exist_ok=True)

    specs = [
        ("yoruba_sample.wav",  3.8, 145.0, 42),
        ("pidgin_sample.wav",  4.5, 175.0, 99),
    ]

    for filename, duration, pitch, seed in specs:
        out = samples_dir / filename
        audio = generate_speech_like(duration=duration, pitch=pitch, seed=seed)
        sf.write(str(out), audio, 22050, subtype="PCM_16")
        print(f"  Generated {out.name}  ({duration}s, pitch={pitch}Hz)")

    print(f"\nAudio files written to {samples_dir}")


if __name__ == "__main__":
    main()
