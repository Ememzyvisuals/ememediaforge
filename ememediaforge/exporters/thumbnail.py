"""
EmemediaForge — Thumbnail generator.
Renders the intro scene at T=0.9s as a static PNG thumbnail.
"""
from __future__ import annotations
from pathlib import Path
from PIL import Image

from ememediaforge.scenes.intro  import IntroScene
from ememediaforge.themes.base   import Theme


def generate_thumbnail(
    theme: Theme,
    width: int,
    height: int,
    title: str,
    description: str = "",
    logo: str | None = None,
    url: str = "",
    output_path: Path | None = None,
) -> Image.Image:
    """
    Render a static thumbnail image at T=0.9s into the intro scene.

    Parameters
    ----------
    output_path : if provided, saves as PNG to this path

    Returns
    -------
    PIL Image (RGB)
    """
    scene = IntroScene(
        theme=theme,
        width=width,
        height=height,
        fps=30,
        title=title,
        description=description,
        logo=logo,
        url=url,
        duration=1.8,
    )
    img = scene.render(local_t=0.9)   # midpoint of intro = fully faded in

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(str(output_path), "PNG", optimize=True)

    return img
