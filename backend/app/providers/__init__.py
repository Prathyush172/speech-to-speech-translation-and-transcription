"""Model provider interfaces and controlled provider failures."""

from app.providers.stt import (
    AudioInput,
    STTProvider,
    STTProviderError,
    STTResult,
)
from app.providers.translation import (
    TranslationProvider,
    TranslationProviderError,
    TranslationResult,
)
from app.providers.tts import (
    ManagedAudioArtifact,
    TTSProvider,
    TTSProviderError,
    TTSResult,
)

__all__ = [
    "AudioInput",
    "ManagedAudioArtifact",
    "STTProvider",
    "STTProviderError",
    "STTResult",
    "TTSProvider",
    "TTSProviderError",
    "TTSResult",
    "TranslationProvider",
    "TranslationProviderError",
    "TranslationResult",
]
