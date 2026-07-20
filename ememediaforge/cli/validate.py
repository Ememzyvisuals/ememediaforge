"""
EmemediaForge — `forge validate` command.
Validates project.yaml and checks all assets exist WITHOUT rendering.
"""

from __future__ import annotations

from pathlib import Path

from rich.console import Console
from rich.table import Table

from ememediaforge.config.loader import load_config, validate_assets_exist
from ememediaforge.core.exceptions import ConfigError

console = Console()


def run_validate(config_path: str) -> bool:
    """
    Validate project.yaml. Returns True if valid, False if errors found.
    Prints a summary table to the terminal.
    """
    path = Path(config_path)
    console.print(f"\n[bold]Validating[/] [cyan]{path}[/]\n")

    # ── Parse YAML ──────────────────────────────────────────────────────────
    try:
        config = load_config(path)
    except ConfigError as e:
        console.print(f"[bold red]  ✗ Config error:[/]\n{e}\n")
        return False

    # ── Print summary ────────────────────────────────────────────────────────
    tbl = Table(show_header=False, box=None, padding=(0, 2))
    tbl.add_column("key", style="dim")
    tbl.add_column("value", style="white")
    tbl.add_row("Project", config.project.name)
    tbl.add_row("Description", config.project.description or "—")
    tbl.add_row("Theme", config.theme)
    tbl.add_row("Template", config.template)
    tbl.add_row("Resolution", config.resolution)
    tbl.add_row("FPS", str(config.fps))
    tbl.add_row("Samples", str(len(config.samples)))
    console.print(tbl)
    console.print()

    # ── Check samples ────────────────────────────────────────────────────────
    console.print("  [bold]Samples:[/]")
    for i, s in enumerate(config.samples, 1):
        audio_ok = "✓" if s.audio.exists() else "✗"
        txt_ok = "✓" if s.transcript.exists() else "✗"
        a_color = "green" if s.audio.exists() else "red"
        t_color = "green" if s.transcript.exists() else "red"
        console.print(
            f"    [{i}] {s.title}\n"
            f"        audio     [{a_color}]{audio_ok}[/] {s.audio}\n"
            f"        transcript[{t_color}]{txt_ok}[/] {s.transcript}"
        )

    # ── Asset check ──────────────────────────────────────────────────────────
    asset_errors = validate_assets_exist(config)
    if asset_errors:
        console.print(f"\n[bold red]  ✗ {len(asset_errors)} asset(s) missing:[/]")
        for e in asset_errors:
            console.print(f"    • {e}")
        return False

    console.print("\n[bold green]  ✓ Config is valid — ready to build.[/]")
    console.print(f"  Run: [bold cyan]forge build {path}[/]\n")
    return True
