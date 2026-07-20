"""
EmemediaForge — Metadata JSON export.
"""
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path

import ememediaforge
from ememediaforge.config.schema import ProjectConfig
from ememediaforge.timeline.timeline import VideoTimeline


def export_metadata(
    config: ProjectConfig,
    timeline: VideoTimeline,
    output_path: Path,
    video_path: Path,
    thumbnail_path: Path,
) -> dict:
    """
    Write metadata.json describing the generated video.

    Returns the metadata dict.
    """
    samples_meta = []
    for spec in timeline.scenes:
        if spec.scene_type != "sample":
            continue
        d = spec.data
        samples_meta.append({
            "title":          d.get("title", ""),
            "audio":          d.get("audio_path", ""),
            "language":       d.get("language", "en"),
            "start_time_sec": spec.start_time,
            "duration_sec":   spec.duration,
        })

    meta = {
        "tool":           "EmemediaForge",
        "version":        ememediaforge.__version__,
        "generated_at":   datetime.now(timezone.utc).isoformat(),
        "project": {
            "name":        config.project.name,
            "description": config.project.description,
            "author":      config.project.author,
            "url":         config.project.url,
        },
        "video": {
            "file":            str(video_path.name),
            "resolution":      config.resolution,
            "fps":             config.fps,
            "duration_sec":    round(timeline.total_duration, 3),
            "theme":           config.theme,
            "template":        config.template,
        },
        "thumbnail": str(thumbnail_path.name),
        "samples":   samples_meta,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    return meta
