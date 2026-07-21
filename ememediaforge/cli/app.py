"""
EmemediaForge — Typer CLI application entry point.

Commands:
  forge init               Scaffold a new project
  forge validate <config>  Validate config without building
  forge build <config>     Full render pipeline
"""

from __future__ import annotations

import typer
from rich.console import Console

import ememediaforge

app = typer.Typer(
    name="forge",
    help=(
        "EmemediaForge — Professional showcase video generator for Speech AI models.\n\n"
        "Built by @Ememzyvisuals (Axiveri) · https://github.com/Ememzyvisuals/ememediaforge"
    ),
    add_completion=False,
    pretty_exceptions_enable=False,
)
console = Console()


@app.command("init")
def cmd_init(
    directory: str = typer.Argument(
        ".", help="Directory to scaffold the project in (default: current directory)"
    ),
) -> None:
    """
    Scaffold a new EmemediaForge project with example project.yaml,
    sample directories, and bundled font download.
    """
    from ememediaforge.cli.init import run_init

    run_init(directory)


@app.command("validate")
def cmd_validate(
    config: str = typer.Argument(..., help="Path to project.yaml"),
) -> None:
    """
    Validate project.yaml and verify all assets exist.
    Does NOT render any video.
    """
    import sys

    from ememediaforge.cli.validate import run_validate

    ok = run_validate(config)
    if not ok:
        sys.exit(1)


@app.command("build")
def cmd_build(
    config: str = typer.Argument(..., help="Path to project.yaml"),
    stable_ts: bool = typer.Option(
        False,
        "--stable-ts / --no-stable-ts",
        help="Use stable-ts for higher-accuracy word alignment (requires: pip install ememediaforge[stable_ts])",
    ),
    output: str | None = typer.Option(
        None, "--output", "-o", help="Override output directory from config (default: dist/)"
    ),
) -> None:
    """
    Build a professional showcase video from project.yaml.

    Outputs:
      dist/demo.mp4        — Final video
      dist/thumbnail.png   — Static thumbnail
      dist/metadata.json   — Build metadata
    """
    from ememediaforge.cli.build import run_build

    run_build(config, stable_ts=stable_ts, output_dir=output, fast=fast)  # noqa: F821


@app.command("version")
def cmd_version() -> None:
    """Print EmemediaForge version."""
    console.print(
        f"[bold magenta]EmemediaForge[/] [dim]v{ememediaforge.__version__}[/]  "
        f"[dim]by @Ememzyvisuals · Axiveri[/]"
    )


def main() -> None:
    """CLI entry point registered as `forge` in pyproject.toml."""
    app()


if __name__ == "__main__":
    main()
