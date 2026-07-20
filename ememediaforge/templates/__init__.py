"""EmemediaForge templates — TTS and STT template configs."""

from ememediaforge.templates.stt import TEMPLATE_ID as STT
from ememediaforge.templates.stt import get_config as stt_config
from ememediaforge.templates.tts import TEMPLATE_ID as TTS
from ememediaforge.templates.tts import get_config as tts_config

__all__ = ["tts_config", "stt_config", "TTS", "STT"]
