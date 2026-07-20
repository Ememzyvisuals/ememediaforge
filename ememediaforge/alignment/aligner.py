"""
EmemediaForge — Lightweight energy-based word aligner.

No ML model required. Uses RMS energy analysis + proportional
character-count distribution to assign word timestamps to audio.

This is ideal for TTS demos (we know exactly what was said) and
works across all languages including Nigerian languages (Yoruba,
Igbo, Hausa, Pidgin) without any language-specific models.

For production-level alignment, install the optional `stable-ts`
extra: `pip install ememediaforge[stable_ts]`
"""

from __future__ import annotations

import re
from pathlib import Path

from ememediaforge.alignment.timestamps import WordTimestamp
from ememediaforge.audio.analyzer import (
    compute_rms,
    find_voiced_segments,
    load_audio,
)
from ememediaforge.core.exceptions import AlignmentError

# ── Public API ────────────────────────────────────────────────────────────────


def align(
    audio_path: Path | str,
    transcript: str,
    sr: int = 22050,
    use_stable_ts: bool = False,
) -> list[WordTimestamp]:
    """
    Align transcript words to audio timestamps.

    Parameters
    ----------
    audio_path    : path to the audio file
    transcript    : plain-text transcript string
    sr            : sample rate to load audio at
    use_stable_ts : if True, attempt to use stable-ts for higher accuracy

    Returns
    -------
    list[WordTimestamp] in sequential order (start-sorted)
    """
    words = _tokenize(transcript)
    if not words:
        raise AlignmentError("Transcript is empty or contains no words.")

    # Attempt stable-ts alignment if requested and available
    if use_stable_ts:
        result = _align_stable_ts(audio_path, transcript)
        if result is not None:
            return result

    # Fall back to energy-based alignment
    return _align_energy(audio_path, words, sr)


# ── Internal helpers ──────────────────────────────────────────────────────────


def _tokenize(transcript: str) -> list[str]:
    """Split transcript into words, stripping punctuation from edges."""
    raw = transcript.strip().split()
    return [re.sub(r"^[^\w]+|[^\w]+$", "", w) for w in raw if w.strip()]


def _even_distribution(words: list[str], duration: float) -> list[WordTimestamp]:
    """Fallback: distribute words evenly across the full audio duration."""
    total_chars = max(1, sum(len(w) for w in words))
    stamps: list[WordTimestamp] = []
    current = 0.0
    for w in words:
        word_dur = max(0.06, (len(w) / total_chars) * duration)
        stamps.append(WordTimestamp(word=w, start=current, end=current + word_dur))
        current += word_dur
    # Clamp final word to audio duration
    if stamps:
        stamps[-1] = WordTimestamp(stamps[-1].word, stamps[-1].start, duration)
    return stamps


def _align_energy(
    audio_path: Path | str,
    words: list[str],
    sr: int = 22050,
) -> list[WordTimestamp]:
    """
    Energy-based alignment:
    1. Find voiced segments via RMS threshold
    2. Distribute words proportionally by character count within speech zones
    3. Include short silence gaps between words for natural pacing
    """
    y, sr = load_audio(audio_path, sr=sr)
    duration = len(y) / sr

    if not words:
        return []

    hop = 512
    rms = compute_rms(y, hop_length=hop)
    segments = find_voiced_segments(rms, sr, hop_length=hop)

    if not segments:
        return _even_distribution(words, duration)

    # Speech boundaries
    speech_start = segments[0][0]
    speech_end = segments[-1][1]
    speech_dur = max(0.1, speech_end - speech_start)

    total_chars = max(1, sum(len(w) for w in words))

    # Inter-word gap: 3% of speech duration, min 30ms, max 120ms
    gap = min(0.12, max(0.03, speech_dur * 0.03 / max(len(words) - 1, 1)))
    available_dur = speech_dur - gap * max(len(words) - 1, 0)

    stamps: list[WordTimestamp] = []
    current = speech_start

    for i, w in enumerate(words):
        word_dur = max(0.06, (len(w) / total_chars) * available_dur)
        stamps.append(WordTimestamp(word=w, start=current, end=current + word_dur))
        current += word_dur + (gap if i < len(words) - 1 else 0)

    # Ensure last word ends exactly at speech_end
    if stamps:
        last = stamps[-1]
        stamps[-1] = WordTimestamp(last.word, last.start, speech_end)

    return stamps


def _align_stable_ts(
    audio_path: Path | str,
    transcript: str,
) -> list[WordTimestamp] | None:
    """
    High-accuracy alignment using stable-ts (optional dependency).
    Returns None if stable-ts is not installed or fails.

    Install: pip install ememediaforge[stable_ts]
    """
    try:
        import stable_whisper  # type: ignore
    except ImportError:
        return None

    try:
        model = stable_whisper.load_model("tiny")  # Smallest model for speed
        result = model.align(str(audio_path), transcript, language="en")
        stamps: list[WordTimestamp] = []
        for seg in result.segments:
            for word in seg.words:
                stamps.append(
                    WordTimestamp(
                        word=word.word.strip(),
                        start=float(word.start),
                        end=float(word.end),
                    )
                )
        return stamps if stamps else None
    except Exception:
        return None
