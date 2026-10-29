"""Typed speech-to-text provider boundary."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, Protocol, runtime_checkable

LanguageCode = Literal["en", "hi"]


@dataclass(frozen=True)
class AudioInput:
    data: bytes
    content_type: str | None = None
    filename: str | Path | None = None


@dataclass(frozen=True)
class STTResult:
    transcript: str
    language: LanguageCode | str | None = None
    confidence: float | None = None
    metadata: dict[str, object] = field(default_factory=dict)


class STTProviderError(Exception):
    """Expected failure raised by an STT provider."""


@runtime_checkable
class STTProvider(Protocol):
    def transcribe(
        self,
        audio: AudioInput | bytes,
        language: LanguageCode | str | None = None,
    ) -> STTResult:
        """Return a typed transcript or raise ``STTProviderError``."""
