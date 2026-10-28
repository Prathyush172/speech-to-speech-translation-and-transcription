"""API router registration."""

from typing import Annotated

from fastapi import APIRouter, Depends, Request

from app.providers.translation import TranslationProvider
from app.schemas.translation import (
    ErrorResponse,
    TranslationRequest,
    TranslationResponse,
)
from app.services.translation_service import translate_text

router = APIRouter()


def get_translation_provider(request: Request) -> TranslationProvider | None:
    """Return the provider configured on the application, if any."""
    return getattr(request.app.state, "translation_provider", None)


@router.get("/health", tags=["health"], summary="Check API health")
def health_check() -> dict[str, str]:
    """Return the service status without initializing model providers."""
    return {"status": "ok"}


@router.post(
    "/translate",
    response_model=TranslationResponse,
    responses={
        422: {"description": "Request validation failed."},
        502: {"model": ErrorResponse, "description": "Translation provider failed."},
        503: {
            "model": ErrorResponse,
            "description": "No translation provider is configured.",
        },
    },
    tags=["translation"],
    summary="Translate typed text",
)
async def translate(
    payload: TranslationRequest,
    provider: Annotated[
        TranslationProvider | None,
        Depends(get_translation_provider),
    ],
) -> TranslationResponse:
    """Translate non-empty English or Hindi text in the selected direction."""
    return await translate_text(payload, provider)
