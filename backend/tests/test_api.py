"""API route registration tests."""

import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import create_app
from app.providers.translation import TranslationDirection, TranslationProviderError


class FakeTranslationProvider:
    """Deterministic provider for endpoint tests."""

    def translate(self, source_text: str, direction: TranslationDirection) -> str:
        return f"{direction}: {source_text}"


class FailingTranslationProvider:
    """Provider test double that simulates a controlled inference failure."""

    def translate(self, source_text: str, direction: TranslationDirection) -> str:
        del source_text, direction
        raise TranslationProviderError("internal provider details")


def test_health_endpoint_is_documented_in_openapi() -> None:
    app = create_app(Settings(_env_file=None))

    with TestClient(app) as client:
        response = client.get("/openapi.json")

    assert response.status_code == 200
    assert "/api/health" in response.json()["paths"]
    openapi = response.json()
    assert "/api/translate" in openapi["paths"]
    operation = openapi["paths"]["/api/translate"]["post"]
    assert operation["requestBody"]["content"]["application/json"]["schema"][
        "$ref"
    ].endswith("/TranslationRequest")
    assert operation["responses"]["200"]["content"]["application/json"]["schema"][
        "$ref"
    ].endswith("/TranslationResponse")
    assert "422" in operation["responses"]
    assert "502" in operation["responses"]
    assert "503" in operation["responses"]


@pytest.mark.parametrize(
    ("direction", "source_text", "source_language", "target_language"),
    [
        ("en-to-hi", "Hello", "en", "hi"),
        ("hi-to-en", "नमस्ते", "hi", "en"),
    ],
)
def test_translate_endpoint_returns_typed_translation(
    direction: str,
    source_text: str,
    source_language: str,
    target_language: str,
) -> None:
    app = create_app(
        Settings(_env_file=None),
        translation_provider=FakeTranslationProvider(),
    )

    with TestClient(app) as client:
        response = client.post(
            "/api/translate",
            json={"direction": direction, "source_text": source_text},
        )

    assert response.status_code == 200
    assert response.json() == {
        "direction": direction,
        "source_text": source_text,
        "source_language": source_language,
        "target_language": target_language,
        "detected_language": None,
        "translated_text": f"{direction}: {source_text}",
        "status": "success",
    }


@pytest.mark.parametrize("source_text", ["", " ", "\t\n"])
def test_translate_endpoint_returns_useful_422_for_empty_text(
    source_text: str,
) -> None:
    app = create_app(
        Settings(_env_file=None),
        translation_provider=FakeTranslationProvider(),
    )

    with TestClient(app) as client:
        response = client.post(
            "/api/translate",
            json={"direction": "en-to-hi", "source_text": source_text},
        )

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert detail[0]["loc"] == ["body", "source_text"]
    assert "at least 1 character" in detail[0]["msg"]


def test_translate_endpoint_rejects_unsupported_direction() -> None:
    app = create_app(
        Settings(_env_file=None),
        translation_provider=FakeTranslationProvider(),
    )

    with TestClient(app) as client:
        response = client.post(
            "/api/translate",
            json={"direction": "en-to-fr", "source_text": "Hello"},
        )

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "direction"]


def test_translate_endpoint_reports_unconfigured_provider_safely() -> None:
    app = create_app(Settings(_env_file=None, provider_mode="real"))

    with TestClient(app) as client:
        response = client.post(
            "/api/translate",
            json={"direction": "en-to-hi", "source_text": "Hello"},
        )

    assert response.status_code == 503
    assert response.json() == {
        "status": "error",
        "code": "translation_provider_unavailable",
        "message": "Translation is not available because no provider is configured.",
        "stage": "translation",
    }


def test_translate_endpoint_reports_provider_failure_without_internal_details() -> None:
    app = create_app(
        Settings(_env_file=None),
        translation_provider=FailingTranslationProvider(),
    )

    with TestClient(app) as client:
        response = client.post(
            "/api/translate",
            json={"direction": "en-to-hi", "source_text": "Hello"},
        )

    assert response.status_code == 502
    assert response.json() == {
        "status": "error",
        "code": "translation_failed",
        "message": "Translation could not be completed.",
        "stage": "translation",
    }
    assert "internal provider details" not in response.text
