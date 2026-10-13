from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Message détaillé de l'erreur renvoyée par l'API.")
    code: str | None = Field(default=None, description="Code applicatif optionnel, utile pour le diagnostic côté client.")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "detail": "La question ne peut pas être vide.",
                "code": "invalid_input",
            }
        }
    )


class HealthStatusResponse(BaseModel):
    status: str = Field(default="ok", description="Statut de santé du service.")
    service: str = Field(..., description="Nom du service backend.")
    version: str = Field(..., description="Version applicative exposée.")
    mode: str = Field(..., description="Mode de fonctionnement courant.")
    environment: str = Field(..., description="Environnement d'exécution.")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "ok",
                "service": "Urgence Santé",
                "version": "0.1.0",
                "mode": "demo",
                "environment": "development",
            }
        }
    )


class RootResponse(BaseModel):
    message: str = Field(..., description="Message de bienvenue de l'API.")
    version: str = Field(..., description="Version applicative exposée.")


class SupportedLanguagesResponse(BaseModel):
    supported: list[str] = Field(..., description="Langues prises en charge par le prototype.")
    note: str = Field(..., description="Précision sur le niveau de support démonstratif.")


class CountryValidationResponse(BaseModel):
    country: str = Field(..., description="Code pays normalisé et validé.")
    valid: bool = Field(..., description="Indique si le code pays est accepté.")


class LanguageValidationResponse(BaseModel):
    language: str = Field(..., description="Langue normalisée et validée.")
    valid: bool = Field(..., description="Indique si la valeur est acceptée par le backend.")


class HealthArticleResult(BaseModel):
    article_id: str = Field(..., description="Identifiant interne de la fiche.")
    title: str = Field(..., description="Titre de la ressource de santé.")
    category: str = Field(..., description="Catégorie thématique de la fiche.")
    source: str = Field(..., description="Nom de la source documentaire.")
    country: str = Field(..., description="Pays cible associé à la fiche.")
    language: str = Field(..., description="Langue de publication de la fiche.")
    content: str = Field(..., description="Contenu textuel de la fiche.")
    status: str = Field(..., description="Statut de validation selon le pipeline de démonstration.")
    last_verified: str | None = Field(default=None, description="Date de dernière vérification de la source.")


class HealthSearchResponse(BaseModel):
    results: list[HealthArticleResult] = Field(..., description="Liste des fiches documentaires correspondantes.")
    count: int = Field(..., description="Nombre total de résultats retournés.")


class HealthSourceResult(BaseModel):
    source_id: str = Field(..., description="Identifiant de source unique.")
    name: str = Field(..., description="Nom de la source documentaire.")
    country: str = Field(..., description="Pays couvert par la source.")
    language: str = Field(..., description="Langue de la source.")
    url: str | None = Field(default=None, description="URL publique de référence, si disponible.")
    last_verified: str | None = Field(default=None, description="Date de dernière vérification de la source.")


class HealthSourcesResponse(BaseModel):
    results: list[HealthSourceResult] = Field(..., description="Sources disponibles pour le contexte demandé.")
    count: int = Field(..., description="Nombre de sources trouvées.")
