"""
EmemediaForge — Pydantic v2 schema for project.yaml validation.

All fields are typed and validated. Errors surface clean messages
before any rendering begins.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field, field_validator

# ---------------------------------------------------------------------------
# Supported values
# ---------------------------------------------------------------------------

VALID_THEMES = {"modern", "light", "dark", "minimal"}
VALID_TEMPLATES = {"tts", "stt"}
VALID_RESOLUTIONS = {"1280x720", "1080x1080", "1080x1920"}
VALID_AUDIO_EXTS = {".wav", ".mp3", ".flac", ".ogg", ".m4a", ".aac"}
VALID_TRANSCRIPT_EXTS = {".txt", ".text"}


# ---------------------------------------------------------------------------
# Sub-models
# ---------------------------------------------------------------------------


class SampleConfig(BaseModel):
    """Configuration for a single audio sample to showcase."""

    title: str = Field(..., description="Label shown on screen, e.g. 'Female Voice'")
    audio: Path = Field(..., description="Path to the audio file (.wav, .mp3, .flac, …)")
    transcript: Path = Field(..., description="Path to the plain-text transcript file")
    language: str = Field("en", description="BCP-47 language code, e.g. 'yo' for Yoruba")

    @field_validator("audio")
    @classmethod
    def validate_audio_extension(cls, v: Path) -> Path:
        if v.suffix.lower() not in VALID_AUDIO_EXTS:
            raise ValueError(
                f"Unsupported audio format '{v.suffix}'. "
                f"Supported: {', '.join(sorted(VALID_AUDIO_EXTS))}"
            )
        return v

    @field_validator("transcript")
    @classmethod
    def validate_transcript_extension(cls, v: Path) -> Path:
        if v.suffix.lower() not in VALID_TRANSCRIPT_EXTS:
            raise ValueError(f"Transcript must be a plain text file (.txt). Got '{v.suffix}'")
        return v


class ProjectMeta(BaseModel):
    """Top-level project metadata."""

    name: str = Field(..., description="Display name for the AI model being showcased")
    description: str = Field("", description="Short description shown in intro/outro scenes")
    author: str = Field("", description="Author or organization name")
    url: str = Field("", description="Project URL (HuggingFace, GitHub, etc.)")


# ---------------------------------------------------------------------------
# Root project config
# ---------------------------------------------------------------------------


class ProjectConfig(BaseModel):
    """
    Full project configuration parsed from project.yaml.

    Example YAML:
        project:
          name: NaijaVox 2.0
          description: Multilingual Nigerian Speech Recognition
          author: Axiveri
          url: https://huggingface.co/Axiveri/NaijaVox-2.0

        theme: dark
        template: stt
        logo: logo.png

        resolution: 1280x720
        fps: 30

        samples:
          - title: Yoruba Sample
            audio: samples/yoruba.wav
            transcript: samples/yoruba.txt
            language: yo
    """

    project: ProjectMeta
    theme: str = Field("modern", description="Visual theme: modern | dark | minimal")
    template: str = Field("tts", description="Video template: tts | stt")
    logo: Path | None = Field(None, description="Path to logo image (PNG, JPG)")
    samples: list[SampleConfig] = Field(..., min_length=1)
    output_dir: Path = Field(Path("dist"), description="Output directory for generated files")
    resolution: str = Field(
        "1280x720", description="Video resolution: 1280x720 | 1080x1080 | 1080x1920"
    )
    fps: int = Field(30, ge=24, le=60, description="Frames per second (24–60)")

    @field_validator("theme")
    @classmethod
    def validate_theme(cls, v: str) -> str:
        v = v.lower().strip()
        if v not in VALID_THEMES:
            raise ValueError(f"Unknown theme '{v}'. Choose from: {', '.join(sorted(VALID_THEMES))}")
        return v

    @field_validator("template")
    @classmethod
    def validate_template(cls, v: str) -> str:
        v = v.lower().strip()
        if v not in VALID_TEMPLATES:
            raise ValueError(
                f"Unknown template '{v}'. Choose from: {', '.join(sorted(VALID_TEMPLATES))}"
            )
        return v

    @field_validator("resolution")
    @classmethod
    def validate_resolution(cls, v: str) -> str:
        if v not in VALID_RESOLUTIONS:
            raise ValueError(
                f"Invalid resolution '{v}'. Supported: {', '.join(sorted(VALID_RESOLUTIONS))}"
            )
        return v

    @field_validator("fps")
    @classmethod
    def validate_fps(cls, v: int) -> int:
        if v not in (24, 25, 30, 50, 60):
            raise ValueError("fps must be one of: 24, 25, 30, 50, 60")
        return v

    def get_resolution_tuple(self) -> tuple[int, int]:
        """Return (width, height) as integers."""
        w, h = self.resolution.split("x")
        return int(w), int(h)
