from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.core.config import APP_ENV, SUPPORTED_LANGUAGES
from app.core.security import normalize_country, normalize_language
from app.schemas.common import (
    CountryValidationResponse,
    ErrorResponse,
    HealthStatusResponse,
    LanguageValidationResponse,
    SupportedLanguagesResponse,
)

router = APIRouter(tags=["health"])


@router.get(
    "/health",
    response_model=HealthStatusResponse,
    summary="Vérifie l'état du service",
    description="Retourne le statut général de l'application pour la supervision et la vérification de disponibilité.",
    responses={
        200: {"description": "Le service est disponible."},
    },
)
def health_check() -> HealthStatusResponse:
    return HealthStatusResponse(
        status="ok",
        service="Urgence Santé",
        version="0.1.0",
        mode="demo",
        environment=APP_ENV,
    )


@router.get(
    "/api/v1/languages",
    response_model=SupportedLanguagesResponse,
    summary="Liste des langues supportées",
    description="Renvoie les langues prises en charge en prototype, sans aucune garantie de conformité médicale ni de traduction fonctionnelle complète.",
)
def list_languages() -> SupportedLanguagesResponse:
    return SupportedLanguagesResponse(
        supported=SUPPORTED_LANGUAGES,
        note="Les langues sont prises en charge en mode démonstration uniquement.",
    )


@router.get(
    "/api/v1/validate-country",
    response_model=CountryValidationResponse,
    summary="Valide un code pays",
    description="Normalise et valide un code pays au format attendu par les endpoints du prototype.",
    responses={
        200: {"description": "Le code pays est valide."},
        400: {"model": ErrorResponse, "description": "Le code pays est invalide ou incomplet."},
    },
)
def validate_country(country: str) -> CountryValidationResponse:
    try:
        normalized_country = normalize_country(country)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return CountryValidationResponse(country=normalized_country, valid=True)


@router.get(
    "/api/v1/validate-language",
    response_model=LanguageValidationResponse,
    summary="Valide une langue supportée",
    description="Normalise et valide une langue sur la liste acceptée par l'application.",
    responses={
        200: {"description": "La langue est valide."},
        400: {"model": ErrorResponse, "description": "La langue n'est pas supportée."},
    },
)
def validate_language(language: str) -> LanguageValidationResponse:
    try:
        normalized_language = normalize_language(language)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return LanguageValidationResponse(language=normalized_language, valid=True)
