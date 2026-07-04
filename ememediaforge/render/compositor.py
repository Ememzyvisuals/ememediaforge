"""
EmemediaForge — Frame compositor.
Routes timeline scenes to the correct Scene subclass and calls render().
"""
from __future__ import annotations
from typing import Iterator
from PIL import Image

from ememediaforge.themes.base import Theme
from ememediaforge.timeline.timeline import SceneSpec, VideoTimeline
from ememediaforge.scenes.intro      import IntroScene
from ememediaforge.scenes.outro      import OutroScene
from ememediaforge.scenes.transition import TransitionScene
from ememediaforge.scenes.sample     import SampleScene
from ememediaforge.audio.analyzer    import get_waveform_frames, load_audio


def _make_scene(spec: SceneSpec, theme: Theme, width: int, height: int,
                fps: int, waveform_cache: dict[int, list[list[float]]]):
    """Instantiate the correct scene object from a SceneSpec."""
    t = spec.scene_type
    d = spec.data

    if t == "intro":
        return IntroScene(
            theme=theme, width=width, height=height, fps=fps,
            title=d.get("title", ""),
            description=d.get("description", ""),
            author=d.get("author", ""),
            url=d.get("url", ""),
            logo=d.get("logo"),
            duration=spec.duration,
        )
    elif t == "outro":
        return OutroScene(
            theme=theme, width=width, height=height, fps=fps,
            title=d.get("title", ""),
            url=d.get("url", ""),
            logo=d.get("logo"),
            duration=spec.duration,
        )
    elif t == "transition":
        return TransitionScene(
            theme=theme, width=width, height=height, fps=fps,
            duration=spec.duration,
        )
    elif t == "sample":
        idx      = d.get("sample_index", 0)
        w_frames = waveform_cache.get(idx, [[0.1] * 64])
        return SampleScene(
            theme=theme, width=width, height=height, fps=fps,
            model_name=d.get("model_name", ""),
            voice_label=d.get("title", ""),
            words=d.get("words", []),
            waveform_frames=w_frames,
            audio_duration=d.get("audio_duration", 3.0),
            sample_index=idx,
            total_samples=d.get("total_samples", 1),
            logo=d.get("logo"),
            template=d.get("template", "tts"),
        )
    else:
        raise ValueError(f"Unknown scene type: {t!r}")


def precompute_waveforms(
    timeline: VideoTimeline,
    fps: int,
) -> dict[int, list[list[float]]]:
    """
    Pre-compute waveform bar data for every sample scene.
    Returns {sample_index: waveform_frames}.
    """
    cache: dict[int, list[list[float]]] = {}
    for spec in timeline.scenes:
        if spec.scene_type != "sample":
            continue
        idx        = spec.data.get("sample_index", 0)
        audio_path = spec.data.get("audio_path", "")
        n_frames   = int(spec.duration * fps) + 1
        try:
            y, sr = load_audio(audio_path, sr=22050)
            cache[idx] = get_waveform_frames(y, sr, n_frames, n_bars=64, fps=fps)
        except Exception:
            cache[idx] = [[0.1] * 64] * n_frames
    return cache


def compose_frames(
    timeline: VideoTimeline,
    theme: Theme,
    width: int,
    height: int,
    fps: int,
    waveform_cache: dict[int, list[list[float]]],
    on_progress=None,
) -> Iterator[Image.Image]:
    """
    Generator that yields one PIL Image per video frame.

    Parameters
    ----------
    on_progress : optional callable(current_frame, total_frames)
    """
    total_dur    = timeline.total_duration
    total_frames = int(total_dur * fps) + 1

    # Cache scene objects (avoid re-instantiating for every frame)
    scene_obj_cache: dict[int, object] = {}

    for frame_idx in range(total_frames):
        global_t = frame_idx / fps
        spec     = timeline.scene_at(global_t)

        if spec is None:
            # Past end of timeline → black frame
            yield Image.new("RGB", (width, height), (0, 0, 0))
            continue

        spec_id = id(spec)
        if spec_id not in scene_obj_cache:
            scene_obj_cache[spec_id] = _make_scene(
                spec, theme, width, height, fps, waveform_cache
            )

        scene    = scene_obj_cache[spec_id]
        local_t  = spec.local_time(global_t)
        frame    = scene.render(local_t)
        yield frame

        if on_progress:
            on_progress(frame_idx + 1, total_frames)
