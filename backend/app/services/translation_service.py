"""Typed-text translation orchestration independent of FastAPI."""

from starlette.concurrency import run_in_threadpool

from app.providers.translation import TranslationProvider, TranslationProviderError
from app.schemas.translation import (
    LanguageCode,
    TranslationDirection,
    TranslationRequest,
    TranslationResponse,
)

LANGUAGES_BY_DIRECTION: dict[
    TranslationDirection, tuple[LanguageCode, LanguageCode]
] = {
    "en-to-hi": ("en", "hi"),
    "hi-to-en": ("hi", "en"),
}


class TranslationServiceError(Exception):
    """Base for expected, client-safe translation service failures."""

    status_code = 502
    code = "translation_failed"
    message = "Translation could not be completed."


class TranslationProviderUnavailable(TranslationServiceError):
    """Raised when no translation provider is configured."""

    status_code = 503
    code = "translation_provider_unavailable"
    message = "Translation is not available because no provider is configured."


class TranslationFailed(TranslationServiceError):
    """Raised when a configured provider cannot produce a translation."""


async def translate_text(
    request: TranslationRequest,
    provider: TranslationProvider | None,
) -> TranslationResponse:
    """Translate validated text using the configured provider."""
    if provider is None:
        raise TranslationProviderUnavailable

    try:
        translated_text = await run_in_threadpool(
            provider.translate,
            request.source_text,
            request.direction,
        )
    except TranslationProviderError as error:
        raise TranslationFailed from error

    if not isinstance(translated_text, str) or not translated_text.strip():
        raise TranslationFailed

    source_language, target_language = LANGUAGES_BY_DIRECTION[request.direction]
    return TranslationResponse(
        direction=request.direction,
        source_text=request.source_text,
        source_language=source_language,
        target_language=target_language,
        translated_text=translated_text,
    )
