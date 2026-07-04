"""
EmemediaForge — Full test suite.
Tests core logic without requiring FFmpeg or real audio files.
"""
from __future__ import annotations
import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
import numpy as np


# ── Config schema ─────────────────────────────────────────────────────────────

def test_project_config_valid(tmp_path):
    from ememediaforge.config.schema import ProjectConfig, ProjectMeta, SampleConfig
    wav = tmp_path / "a.wav"; wav.touch()
    txt = tmp_path / "a.txt"; txt.touch()
    cfg = ProjectConfig(
        project=ProjectMeta(name="TestModel"),
        theme="dark", template="tts",
        samples=[SampleConfig(title="Test", audio=wav, transcript=txt)],
    )
    assert cfg.project.name == "TestModel"
    assert cfg.theme == "dark"
    assert len(cfg.samples) == 1


def test_invalid_theme_raises():
    from pydantic import ValidationError
    from ememediaforge.config.schema import ProjectConfig, ProjectMeta
    with pytest.raises(ValidationError):
        ProjectConfig(project=ProjectMeta(name="X"), theme="neon_rainbow", samples=[])


def test_resolution_tuple(tmp_path):
    """Build a real model — don't use __new__ to bypass pydantic."""
    from ememediaforge.config.schema import ProjectConfig, ProjectMeta, SampleConfig
    wav = tmp_path / "a.wav"; wav.touch()
    txt = tmp_path / "a.txt"; txt.touch()
    cfg = ProjectConfig(
        project=ProjectMeta(name="X"),
        resolution="1280x720",
        samples=[SampleConfig(title="T", audio=wav, transcript=txt)],
    )
    assert cfg.get_resolution_tuple() == (1280, 720)


def test_resolution_1080(tmp_path):
    from ememediaforge.config.schema import ProjectConfig, ProjectMeta, SampleConfig
    wav = tmp_path / "a.wav"; wav.touch()
    txt = tmp_path / "a.txt"; txt.touch()
    cfg = ProjectConfig(
        project=ProjectMeta(name="X"),
        resolution="1080x1080",
        samples=[SampleConfig(title="T", audio=wav, transcript=txt)],
    )
    assert cfg.get_resolution_tuple() == (1080, 1080)


# ── YAML loader ───────────────────────────────────────────────────────────────

def test_load_config_missing_file():
    from ememediaforge.config.loader import load_config
    from ememediaforge.core.exceptions import ConfigError
    with pytest.raises(ConfigError, match="not found"):
        load_config("/nonexistent/path.yaml")


def test_load_config_valid(tmp_path):
    from ememediaforge.config.loader import load_config
    wav = tmp_path / "a.wav"; wav.touch()
    txt = tmp_path / "a.txt"; txt.touch()
    (tmp_path / "project.yaml").write_text(f"""
project:
  name: TestModel
  description: A test
theme: light
template: stt
samples:
  - title: Voice A
    audio: a.wav
    transcript: a.txt
""")
    cfg = load_config(tmp_path / "project.yaml")
    assert cfg.project.name == "TestModel"
    assert cfg.theme == "light"
    assert cfg.template == "stt"


# ── Themes ────────────────────────────────────────────────────────────────────

def test_all_four_themes():
    from ememediaforge.themes import get_theme, list_themes
    assert set(list_themes()) == {"modern", "light", "dark", "minimal"}
    for name in list_themes():
        t = get_theme(name)
        assert t.name == name
        assert len(t.bg_color) == 3
        assert len(t.accent_color) == 3
        assert len(t.overlay_color) == 4


def test_theme_dark_neon_green():
    from ememediaforge.themes import get_theme
    t = get_theme("dark")
    assert t.bg_color[0] < 30         # near-black background
    assert t.accent_color == (0, 255, 136)  # neon green


def test_theme_light_blue_accent():
    from ememediaforge.themes import get_theme
    t = get_theme("light")
    assert t.bg_color == (255, 255, 255)   # pure white
    assert t.accent_color == (37, 99, 235) # electric blue


def test_theme_modern_purple():
    from ememediaforge.themes import get_theme
    t = get_theme("modern")
    assert t.bg_color == (255, 255, 255)
    assert t.accent_color == (124, 58, 237)


def test_theme_unknown_raises():
    from ememediaforge.themes import get_theme
    with pytest.raises(ValueError, match="Unknown theme"):
        get_theme("vaporwave")


# ── Alignment ─────────────────────────────────────────────────────────────────

def test_word_timestamp_properties():
    from ememediaforge.alignment import WordTimestamp
    wt = WordTimestamp(word="hello", start=1.0, end=1.5)
    assert wt.is_active(1.2)   is True
    assert wt.is_active(0.9)   is False
    assert wt.is_active(1.5)   is False   # end is exclusive
    assert wt.is_past(2.0)     is True
    assert wt.is_future(0.5)   is True
    assert wt.duration == pytest.approx(0.5)


def test_align_energy_word_count(tmp_path):
    import soundfile as sf
    from ememediaforge.alignment import align
    sr = 22050
    y  = (np.sin(2 * np.pi * 440 * np.linspace(0, 2, 2*sr)) * 0.5).astype(np.float32)
    wav = tmp_path / "test.wav"
    sf.write(str(wav), y, sr)
    words = align(wav, "hello world naija", use_stable_ts=False)
    assert len(words) == 3
    assert [w.word for w in words] == ["hello", "world", "naija"]


def test_align_returns_ordered_timestamps(tmp_path):
    import soundfile as sf
    from ememediaforge.alignment import align
    sr = 22050
    y  = (np.sin(2 * np.pi * 440 * np.linspace(0, 3, 3*sr)) * 0.5).astype(np.float32)
    wav = tmp_path / "t.wav"; sf.write(str(wav), y, sr)
    words = align(wav, "one two three four five", use_stable_ts=False)
    starts = [w.start for w in words]
    assert starts == sorted(starts), "Timestamps must be monotonically increasing"
    assert all(w.start < w.end for w in words), "start must always be < end"


# ── Timeline ─────────────────────────────────────────────────────────────────

def test_timeline_scene_at():
    from ememediaforge.timeline import SceneSpec, VideoTimeline
    tl = VideoTimeline(scenes=[
        SceneSpec("intro",  0.0, 1.5),
        SceneSpec("sample", 1.5, 3.0),
        SceneSpec("outro",  4.5, 2.0),
    ])
    assert tl.scene_at(0.5).scene_type  == "intro"
    assert tl.scene_at(2.0).scene_type  == "sample"
    assert tl.scene_at(5.0).scene_type  == "outro"
    assert tl.total_duration             == pytest.approx(6.5)


def test_build_timeline_structure(tmp_path):
    from ememediaforge.config.schema import ProjectConfig, ProjectMeta, SampleConfig
    from ememediaforge.timeline import build_timeline

    wav1 = tmp_path / "a.wav"; wav1.touch()
    txt1 = tmp_path / "a.txt"; txt1.touch()
    wav2 = tmp_path / "b.wav"; wav2.touch()
    txt2 = tmp_path / "b.txt"; txt2.touch()

    cfg = ProjectConfig(
        project=ProjectMeta(name="NaijaVox", description="", author="", url=""),
        theme="dark", template="stt",
        samples=[
            SampleConfig(title="Yoruba", audio=wav1, transcript=txt1),
            SampleConfig(title="Hausa",  audio=wav2, transcript=txt2),
        ],
    )
    tl = build_timeline(cfg, {0: 2.5, 1: 3.0}, {0: [], 1: []})
    types = [s.scene_type for s in tl.scenes]

    assert types[0]  == "intro"
    assert types[-1] == "outro"
    assert types.count("sample") == 2
    assert types.count("transition") == 1   # between 2 samples
    assert len(tl.audio_timings()) == 2


def test_timeline_local_time():
    from ememediaforge.timeline import SceneSpec
    spec = SceneSpec("sample", start_time=5.0, duration=3.0)
    assert spec.local_time(5.0) == pytest.approx(0.0)
    assert spec.local_time(6.5) == pytest.approx(1.5)
    assert spec.progress(6.5)   == pytest.approx(0.5)


# ── Scene rendering ───────────────────────────────────────────────────────────

def test_intro_scene_renders_rgb(tmp_path):
    from ememediaforge.themes import get_theme
    from ememediaforge.scenes import IntroScene
    from PIL import Image
    for theme_name in ["modern", "light", "dark", "minimal"]:
        scene = IntroScene(get_theme(theme_name), 320, 180, fps=30,
                           title="NaijaVox", description="Test", duration=1.8)
        frame = scene.render(local_t=0.9)
        assert isinstance(frame, Image.Image)
        assert frame.size == (320, 180)
        assert frame.mode == "RGB"


def test_outro_scene_renders(tmp_path):
    from ememediaforge.themes import get_theme
    from ememediaforge.scenes import OutroScene
    scene = OutroScene(get_theme("dark"), 320, 180, fps=30,
                       title="NaijaVox", url="https://hf.co", duration=2.0)
    frame = scene.render(local_t=1.0)
    assert frame.size == (320, 180)


def test_transition_scene_is_dark_at_midpoint():
    from ememediaforge.themes import get_theme
    from ememediaforge.scenes import TransitionScene
    import numpy as np
    scene = TransitionScene(get_theme("modern"), 320, 180, fps=30, duration=0.4)
    mid   = scene.render(local_t=0.2)  # midpoint → near black
    arr   = np.array(mid)
    assert arr.mean() < 80, "Midpoint of dip-to-black transition should be very dark"


# ── Audio / waveform ─────────────────────────────────────────────────────────

def test_get_waveform_frames_shape():
    from ememediaforge.audio.analyzer import get_waveform_frames
    sr  = 22050
    y   = np.random.randn(sr * 2).astype(np.float32)
    frames = get_waveform_frames(y, sr, total_video_frames=60, n_bars=32, fps=30)
    assert len(frames) == 60
    assert len(frames[0]) == 32
    assert all(0.0 <= v <= 1.001 for v in frames[0])


def test_format_duration():
    from ememediaforge.audio.duration import format_duration
    assert format_duration(90) == "01:30"
    assert format_duration(65) == "01:05"
    assert format_duration(9)  == "00:09"
