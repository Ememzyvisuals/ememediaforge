"""
EmemediaForge — YAML configuration loader.

Loads project.yaml, merges relative paths against the config file's
directory, and returns a validated ProjectConfig.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from ememediaforge.config.schema import ProjectConfig
from ememediaforge.core.exceptions import ConfigError


def _resolve_paths(config_dir: Path, data: dict[str, Any]) -> dict[str, Any]:
    """
    Walk the raw YAML dict and resolve all path-like fields relative to
    the directory containing project.yaml.
    """
    # Resolve top-level logo
    if "logo" in data and data["logo"]:
        data["logo"] = str(config_dir / data["logo"])

    # Resolve sample audio + transcript paths
    samples = data.get("samples", [])
    for sample in samples:
        if "audio" in sample and sample["audio"]:
            sample["audio"] = str(config_dir / sample["audio"])
        if "transcript" in sample and sample["transcript"]:
            sample["transcript"] = str(config_dir / sample["transcript"])

    # Resolve output_dir
    if "output_dir" in data and data["output_dir"]:
        data["output_dir"] = str(config_dir / data["output_dir"])

    return data


def load_config(config_path: str | Path) -> ProjectConfig:
    """
    Load and validate a project.yaml file.

    Parameters
    ----------
    config_path : path to the YAML file (e.g. 'project.yaml')

    Returns
    -------
    ProjectConfig — fully validated configuration object

    Raises
    ------
    ConfigError — on missing file, YAML parse error, or schema violation
    """
    path = Path(config_path).resolve()

    if not path.exists():
        raise ConfigError(f"Config file not found: {path}")

    if path.suffix.lower() not in (".yaml", ".yml"):
        raise ConfigError(
            f"Config file must be a YAML file (.yaml or .yml), got: {path.name}"
        )

    # ── Parse YAML ──────────────────────────────────────────────────────────
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw: dict[str, Any] = yaml.safe_load(f) or {}
    except yaml.YAMLError as e:
        raise ConfigError(f"YAML parse error in {path.name}:\n{e}") from e

    # ── Resolve relative paths ───────────────────────────────────────────────
    config_dir = path.parent
    raw = _resolve_paths(config_dir, raw)

    # ── Pydantic validation ──────────────────────────────────────────────────
    try:
        config = ProjectConfig.model_validate(raw)
    except ValidationError as e:
        # Format pydantic v2 errors into human-readable messages
        errors = []
        for err in e.errors():
            loc = " → ".join(str(x) for x in err["loc"])
            msg = err["msg"]
            errors.append(f"  [{loc}] {msg}")
        raise ConfigError(
            f"Invalid configuration in {path.name}:\n" + "\n".join(errors)
        ) from e

    return config


def validate_assets_exist(config: ProjectConfig) -> list[str]:
    """
    Check that all referenced files actually exist on disk.

    Returns a list of human-readable error messages (empty = all good).
    """
    errors: list[str] = []

    # Logo
    if config.logo and not config.logo.exists():
        errors.append(f"Logo not found: {config.logo}")

    # Samples
    for i, sample in enumerate(config.samples, start=1):
        if not sample.audio.exists():
            errors.append(f"Sample #{i} audio not found: {sample.audio}")
        if not sample.transcript.exists():
            errors.append(f"Sample #{i} transcript not found: {sample.transcript}")

    return errors
