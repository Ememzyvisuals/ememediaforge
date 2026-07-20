"""
EmemediaForge — Timeline scheduler.
Assembles scenes from project config into a VideoTimeline.
"""

from __future__ import annotations

from ememediaforge.alignment.timestamps import WordTimestamp
from ememediaforge.config.schema import ProjectConfig
from ememediaforge.timeline.timeline import SceneSpec, VideoTimeline

# Duration constants (seconds)
INTRO_DUR = 1.8
OUTRO_DUR = 2.0
TRANSITION = 0.45  # crossfade between samples
SAMPLE_PAD = 0.40  # silence pad after each sample audio


def build_timeline(
    config: ProjectConfig,
    sample_durations: dict[int, float],
    sample_words: dict[int, list[WordTimestamp]],
) -> VideoTimeline:
    """
    Build the full video timeline from project config and pre-computed data.

    Parameters
    ----------
    config           : validated ProjectConfig
    sample_durations : {sample_index → audio_duration_seconds}
    sample_words     : {sample_index → list[WordTimestamp]}

    Returns
    -------
    VideoTimeline — ordered list of SceneSpecs
    """
    scenes: list[SceneSpec] = []
    cursor = 0.0

    # ── Intro Scene ──────────────────────────────────────────────────────────
    scenes.append(
        SceneSpec(
            scene_type="intro",
            start_time=cursor,
            duration=INTRO_DUR,
            data={
                "title": config.project.name,
                "description": config.project.description,
                "author": config.project.author,
                "url": config.project.url,
                "logo": str(config.logo) if config.logo else None,
            },
        )
    )
    cursor += INTRO_DUR

    # ── Sample Scenes + Transitions ──────────────────────────────────────────
    n_samples = len(config.samples)
    for i, sample in enumerate(config.samples):
        audio_dur = sample_durations.get(i, 3.0)
        scene_dur = audio_dur + SAMPLE_PAD

        scenes.append(
            SceneSpec(
                scene_type="sample",
                start_time=cursor,
                duration=scene_dur,
                data={
                    "title": sample.title,
                    "audio_path": str(sample.audio),
                    "audio_duration": audio_dur,
                    "words": sample_words.get(i, []),
                    "language": sample.language,
                    "sample_index": i,
                    "total_samples": n_samples,
                    "model_name": config.project.name,
                    "logo": str(config.logo) if config.logo else None,
                    "template": config.template,
                },
            )
        )
        cursor += scene_dur

        # Add transition between samples (not after the last one)
        if i < n_samples - 1:
            scenes.append(
                SceneSpec(
                    scene_type="transition",
                    start_time=cursor,
                    duration=TRANSITION,
                    data={},
                )
            )
            cursor += TRANSITION

    # ── Outro Scene ──────────────────────────────────────────────────────────
    scenes.append(
        SceneSpec(
            scene_type="outro",
            start_time=cursor,
            duration=OUTRO_DUR,
            data={
                "title": config.project.name,
                "url": config.project.url,
                "logo": str(config.logo) if config.logo else None,
            },
        )
    )
    cursor += OUTRO_DUR

    return VideoTimeline(scenes=scenes)
