from __future__ import annotations

from app.core.security import normalize_country, normalize_language, sanitize_text
from app.database.session import init_db
from app.models.health_article import HealthArticle
from app.repositories.health_repository import HealthRepository


class HealthKnowledgeBase:
    def __init__(self) -> None:
        init_db()
        self.repository = HealthRepository(articles=[
            HealthArticle(
                article_id="hydration-01",
                title="Hydratation de base",
                category="prévention",
                content="Boire de l'eau régulièrement et ajuster l'apport selon la chaleur et l'activité physique. Ne pas remplacer les conseils médicaux par des régimes personnalisés.",
                country="SN",
                language="fr",
                source_name="Contenu de démonstration non référencé",
                source_url=None,
                publication_date=None,
                last_verified=None,
                reviewer=None,
                status="demo_only",
                version="1.0",
                next_revision=None,
                is_demo=True,
            ),
            HealthArticle(
                article_id="sleep-01",
                title="Sommeil et repos",
                category="bien-être",
                content="Un sommeil régulier et une réduction du stress favorisent la récupération. Les conseils sont généraux et non thérapeutiques.",
                country="SN",
                language="fr",
                source_name="Contenu de démonstration non référencé",
                source_url=None,
                publication_date=None,
                last_verified=None,
                reviewer=None,
                status="demo_only",
                version="1.0",
                next_revision=None,
                is_demo=True,
            ),
        ])
        self.repository.seed_default()

    def _matches_filters(self, article: HealthArticle, *, country: str = "SN", language: str = "fr") -> bool:
        normalized_country = normalize_country(country)
        normalized_language = normalize_language(language)
        article_country_allowed = normalized_country == "ALL" or article.country == normalized_country or article.country == "ALL"
        article_language_base = article.language.split("-")[0].lower()
        requested_language_base = normalized_language.split("-")[0]
        article_language_allowed = article.language.lower() == normalized_language or article_language_base == requested_language_base
        return article_country_allowed and article_language_allowed

    def list_sources(self, *, country: str = "SN", language: str = "fr") -> list[dict]:
        sources: list[dict] = []
        seen: set[str] = set()
        for article in self.repository.get_all():
            if not self._matches_filters(article, country=country, language=language):
                continue
            source_id = article.source_name.lower()
            if source_id in seen:
                continue
            seen.add(source_id)
            sources.append(
                {
                    "source_id": article.article_id,
                    "name": article.source_name,
                    "country": article.country,
                    "language": article.language,
                    "url": article.source_url,
                    "last_verified": article.last_verified.isoformat() if article.last_verified else None,
                }
            )
        return sources

    def search(self, query: str, *, country: str = "SN", language: str = "fr") -> list[dict]:
        cleaned_query = sanitize_text(query)
        if not cleaned_query:
            return []

        articles = self.repository.search(cleaned_query, country=country, language=language)
        return [
            {
                "article_id": article.article_id,
                "title": article.title,
                "category": article.category,
                "source": article.source_name,
                "country": article.country,
                "language": article.language,
                "content": article.content,
                "status": article.status,
                "last_verified": article.last_verified.isoformat() if article.last_verified else None,
            }
            for article in articles
        ]
