"""EmemediaForge templates — TTS and STT template configs."""
from ememediaforge.templates.tts import get_config as tts_config, TEMPLATE_ID as TTS
from ememediaforge.templates.stt import get_config as stt_config, TEMPLATE_ID as STT
__all__ = ["tts_config","stt_config","TTS","STT"]
