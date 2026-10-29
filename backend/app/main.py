"""FastAPI application entry point."""

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routes import router
from app.core.config import Settings, get_settings
from app.core.logging_config import configure_logging
from app.providers.fake import (
    FakeSTTProvider,
    FakeTranslationProvider,
    FakeTTSProvider,
)
from app.providers.faster_whisper_stt import FasterWhisperSTTProvider
from app.providers.stt import STTProvider
from app.providers.translation import TranslationProvider
from app.services.translation_service import TranslationServiceError

logger = logging.getLogger(__name__)


def create_app(
    settings: Settings | None = None,
    translation_provider: TranslationProvider | None = None,
    stt_provider: STTProvider | None = None,
) -> FastAPI:
    """Create the API application without loading any speech models."""
    app_settings = settings or get_settings()
    configure_logging(app_settings.log_level)

    @asynccontextmanager
    async def lifespan(application: FastAPI) -> AsyncIterator[None]:
        application.state.settings = app_settings
        logger.info("Starting speech translation API")
        try:
            yield
        finally:
            logger.info("Shutting down speech translation API")

    application = FastAPI(
        title="English ↔ Hindi Speech Translation API",
        description="Local-first speech translation and transcription service.",
        version="0.1.0",
        lifespan=lifespan,
    )
    if app_settings.provider_mode == "mock":
        application.state.stt_provider = FakeSTTProvider()
        application.state.translation_provider = (
            translation_provider or FakeTranslationProvider()
        )
        application.state.tts_provider = FakeTTSProvider()
    else:
        application.state.stt_provider = stt_provider or FasterWhisperSTTProvider(
            model_id=app_settings.stt_model_id,
            device=app_settings.device,
            compute_type=app_settings.stt_compute_type,
            cache_dir=app_settings.model_cache_dir,
        )
        application.state.translation_provider = translation_provider
        application.state.tts_provider = None

    @application.exception_handler(TranslationServiceError)
    async def handle_translation_error(
        request: Request, error: TranslationServiceError
    ) -> JSONResponse:
        del request
        return JSONResponse(
            status_code=error.status_code,
            content={
                "status": "error",
                "code": error.code,
                "message": error.message,
                "stage": "translation",
            },
        )

    application.include_router(router, prefix="/api")
    return application


app = create_app()
