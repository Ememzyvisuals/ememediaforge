"""
EmemediaForge — Asset loader: fonts, logos, and bundled resources.

Font priority:
  1. Inter (downloaded at forge init to ~/.ememediaforge/fonts/)
  2. Bundled LiberationSans (grotesk, ships with the package)
  3. System DejaVu Sans
  4. PIL default bitmap (last resort)
"""

from __future__ import annotations

import os
import urllib.request
from pathlib import Path
from typing import Optional

from PIL import Image, ImageFont

# ── Paths ────────────────────────────────────────────────────────────────────
_PKG_FONTS = Path(__file__).parent / "fonts"
_USER_FONTS = Path.home() / ".ememediaforge" / "fonts"

# Inter font URLs (SIL Open Font License, safe to download and bundle)
_INTER_URLS = {
    "regular": "https://github.com/rsms/inter/releases/download/v4.0/Inter-4.0.zip",
    # We use direct file URLs as fallback
}

_INTER_DIRECT = {
    "regular": (
        "https://raw.githubusercontent.com/google/fonts/main/ofl/inter/static/"
        "Inter-Regular.ttf"
    ),
    "bold": (
        "https://raw.githubusercontent.com/google/fonts/main/ofl/inter/static/"
        "Inter-Bold.ttf"
    ),
    "medium": (
        "https://raw.githubusercontent.com/google/fonts/main/ofl/inter/static/"
        "Inter-Medium.ttf"
    ),
}


class FontManager:
    """Manages font loading with fallback chain."""

    _cache: dict[tuple, ImageFont.FreeTypeFont] = {}

    @staticmethod
    def get_font(size: int, weight: str = "regular") -> ImageFont.FreeTypeFont:
        """
        Return a PIL ImageFont at the given size and weight.

        Parameters
        ----------
        size   : point size (e.g. 32)
        weight : 'regular', 'bold', or 'medium'
        """
        cache_key = (size, weight)
        if cache_key in FontManager._cache:
            return FontManager._cache[cache_key]

        font_path = FontManager._resolve_font_path(weight)
        try:
            font = ImageFont.truetype(str(font_path), size)
        except Exception:
            # PIL default bitmap font as absolute last resort
            font = ImageFont.load_default()

        FontManager._cache[cache_key] = font
        return font

    @staticmethod
    def _resolve_font_path(weight: str) -> Path:
        """Find the best available font file for the given weight."""
        # 1. Inter in user cache
        inter_map = {
            "regular": "Inter-Regular.ttf",
            "bold": "Inter-Bold.ttf",
            "medium": "Inter-Medium.ttf",
        }
        user_inter = _USER_FONTS / inter_map.get(weight, "Inter-Regular.ttf")
        if user_inter.exists():
            return user_inter

        # 2. Bundled LiberationSans (grotesk fallback, ships with package)
        lib_map = {
            "regular": "LiberationSans-Regular.ttf",
            "bold": "LiberationSans-Bold.ttf",
            "medium": "LiberationSans-Regular.ttf",
        }
        bundled = _PKG_FONTS / lib_map.get(weight, "LiberationSans-Regular.ttf")
        if bundled.exists():
            return bundled

        # 3. DejaVu Sans bundled
        dejavusans = _PKG_FONTS / "DejaVuSans.ttf"
        if dejavusans.exists():
            return dejavusans

        # 4. System fonts fallback
        system_paths = [
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/System/Library/Fonts/Helvetica.ttc",  # macOS
            "C:/Windows/Fonts/arial.ttf",            # Windows
        ]
        for p in system_paths:
            if Path(p).exists():
                return Path(p)

        # No font found — return a dummy path (PIL will fall back to default)
        return Path("none")

    @staticmethod
    def download_inter(show_progress: bool = True) -> bool:
        """
        Download Inter font files to ~/.ememediaforge/fonts/.
        Called by `forge init`.

        Returns True on success, False on failure.
        """
        _USER_FONTS.mkdir(parents=True, exist_ok=True)
        success = True

        for weight, url in _INTER_DIRECT.items():
            filename = f"Inter-{weight.capitalize()}.ttf"
            dest = _USER_FONTS / filename
            if dest.exists():
                continue
            try:
                if show_progress:
                    print(f"  Downloading Inter {weight.capitalize()}…", end=" ", flush=True)
                urllib.request.urlretrieve(url, dest)
                if show_progress:
                    print("✓")
            except Exception as e:
                if show_progress:
                    print(f"✗ ({e})")
                success = False

        return success


def load_logo(logo_path: Path, size: tuple[int, int] = (80, 80)) -> Optional[Image.Image]:
    """
    Load and resize a logo image.

    Parameters
    ----------
    logo_path : Path to the logo image (PNG, JPG, etc.)
    size      : Target (width, height) in pixels

    Returns None if logo_path doesn't exist or fails to load.
    """
    if not logo_path or not logo_path.exists():
        return None
    try:
        img = Image.open(logo_path).convert("RGBA")
        img.thumbnail(size, Image.LANCZOS)
        return img
    except Exception:
        return None
