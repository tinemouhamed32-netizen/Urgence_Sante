from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from app.schemas.common import ErrorResponse, HealthSearchResponse, HealthSourcesResponse
from app.services.health_service import HealthService

router = APIRouter(prefix="/api/v1/health-information", tags=["health_information"])
health_service = HealthService()


@router.get(
    "/search",
    response_model=HealthSearchResponse,
    summary="Recherche une information de santé",
    description="Cherche dans le corpus documentaire démonstratif les contenus correspondant à la requête utilisateur et au contexte pays/langue.",
    responses={
        200: {"description": "Liste des résultats documentaires trouvés."},
        400: {"model": ErrorResponse, "description": "Le texte de recherche est vide ou invalide."},
        404: {"model": ErrorResponse, "description": "Aucune fiche n'a été trouvée pour cette requête."},
    },
)
def search_health_information(
    q: str = Query(..., min_length=1, max_length=200, description="Terme ou phrase de recherche sur le corpus santé."),
    country: str = Query(default="SN", description="Code pays à utiliser pour le filtrage."),
    language: str = Query(default="fr", description="Langue de réponse voulue."),
) -> dict:
    try:
        return health_service.search(q, country=country, language=language)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get(
    "/sources",
    response_model=HealthSourcesResponse,
    summary="Liste les sources de santé attendues",
    description="Retourne les sources de démonstration disponibles pour le pays et la langue demandés.",
    responses={
        200: {"description": "Liste des sources disponibles dans le contexte demandé."},
        400: {"model": ErrorResponse, "description": "Le contexte pays/langue est invalide."},
    },
)
def list_sources(
    country: str = Query(default="SN", description="Code pays pour filtrer les sources."),
    language: str = Query(default="fr", description="Langue demandée pour les sources."),
) -> dict:
    try:
        return health_service.list_sources(country=country, language=language)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
