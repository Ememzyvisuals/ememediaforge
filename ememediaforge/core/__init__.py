"""EmemediaForge core — pipeline orchestrator and exceptions.

Imports are lazy to avoid circular dependency between config ↔ core.
"""

from ememediaforge.core.exceptions import (
    AlignmentError,
    AssetNotFoundError,
    AudioProcessingError,
    ConfigError,
    ExportError,
    FFmpegError,
    ForgeError,
    RenderError,
    TemplateError,
    ThemeError,
)

__all__ = [
    "ForgeError",
    "ConfigError",
    "AssetNotFoundError",
    "AudioProcessingError",
    "AlignmentError",
    "RenderError",
    "FFmpegError",
    "ThemeError",
    "TemplateError",
    "ExportError",
]


def run_pipeline(*args, **kwargs):
    """Lazy import wrapper — avoids circular import at module load time."""
    from ememediaforge.core.pipeline import run_pipeline as _run

    return _run(*args, **kwargs)
