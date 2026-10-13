from __future__ import annotations

from app.core.security import normalize_country, normalize_language, sanitize_text
from app.services.health_knowledge_base import HealthKnowledgeBase


class HealthService:
    def __init__(self, knowledge_base: HealthKnowledgeBase | None = None) -> None:
        self.knowledge_base = knowledge_base or HealthKnowledgeBase()

    def validate_query(self, query: str) -> str:
        cleaned = sanitize_text(query)
        if not cleaned:
            raise ValueError("La requête de recherche ne peut pas être vide.")
        return cleaned

    def validate_context(self, country: str, language: str) -> tuple[str, str]:
        return normalize_country(country), normalize_language(language)

    def search(self, query: str, *, country: str = "SN", language: str = "fr") -> dict:
        cleaned_query = self.validate_query(query)
        normalized_country, normalized_language = self.validate_context(country, language)
        results = self.knowledge_base.search(cleaned_query, country=normalized_country, language=normalized_language)
        if not results:
            raise LookupError("Aucune fiche approuvée n'a été trouvée pour cette recherche.")
        return {"results": results, "count": len(results)}

    def list_sources(self, *, country: str = "SN", language: str = "fr") -> dict:
        normalized_country, normalized_language = self.validate_context(country, language)
        sources = self.knowledge_base.list_sources(country=normalized_country, language=normalized_language)
        return {"results": sources, "count": len(sources)}
