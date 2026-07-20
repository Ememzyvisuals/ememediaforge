"""
EmemediaForge — Project state container.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from ememediaforge.config.schema import ProjectConfig


@dataclass
class ForgeProject:
    """Loaded project state, passed through the pipeline."""
    config: ProjectConfig
    config_path: Path
    sample_durations: dict[int, float] = field(default_factory=dict)
    sample_words: dict[int, list] = field(default_factory=dict)

    @property
    def project_dir(self) -> Path:
        return self.config_path.parent
