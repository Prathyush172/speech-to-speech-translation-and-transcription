"""Model provider interfaces and development providers."""

from app.providers.fake import FakeSTTProvider, FakeTTSProvider, FakeTranslationProvider
from app.providers.stt import AudioInput, STTProvider, STTProviderError, STTResult
from app.providers.translation import TranslationProvider, TranslationProviderError
from app.providers.tts import ManagedAudioArtifact, TTSProvider, TTSProviderError, TTSResult

__all__ = [
    "AudioInput",
    "FakeSTTProvider",
    "FakeTTSProvider",
    "FakeTranslationProvider",
    "ManagedAudioArtifact",
    "STTProvider",
    "STTProviderError",
    "STTResult",
    "TTSProvider",
    "TTSProviderError",
    "TTSResult",
    "TranslationProvider",
    "TranslationProviderError",
]
