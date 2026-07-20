"""
EmemediaForge — Custom exceptions for clear, actionable error reporting.
"""


class ForgeError(Exception):
    """Base exception for all EmemediaForge errors."""
    pass


class ConfigError(ForgeError):
    """Raised when the project.yaml configuration is invalid or missing."""
    pass


class AssetNotFoundError(ForgeError):
    """Raised when a referenced asset file (audio, logo, transcript) cannot be found."""
    pass


class AudioProcessingError(ForgeError):
    """Raised when audio analysis or loading fails."""
    pass


class AlignmentError(ForgeError):
    """Raised when word-to-audio alignment fails."""
    pass


class RenderError(ForgeError):
    """Raised when frame rendering fails."""
    pass


class FFmpegError(ForgeError):
    """Raised when FFmpeg is not installed, not found in PATH, or fails during encoding."""
    pass


class ThemeError(ForgeError):
    """Raised when an invalid theme name is specified."""
    pass


class TemplateError(ForgeError):
    """Raised when an invalid template name is specified."""
    pass


class ExportError(ForgeError):
    """Raised when exporting assets (MP4, thumbnail, metadata) fails."""
    pass
