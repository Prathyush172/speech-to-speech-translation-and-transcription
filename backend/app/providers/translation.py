"""Translation provider interface and expected provider errors."""

from typing import Protocol

from app.schemas.translation import TranslationDirection


class TranslationProviderError(Exception):
    """Expected failure raised by a translation provider."""


class TranslationProvider(Protocol):
    """Translate source text in one of the supported directions."""

    def translate(self, source_text: str, direction: TranslationDirection) -> str:
        """Return translated text or raise ``TranslationProviderError``."""
