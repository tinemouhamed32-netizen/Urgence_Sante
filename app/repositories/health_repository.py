from __future__ import annotations

import math
import re
import unicodedata

from app.core.security import normalize_country, normalize_language, sanitize_text
from app.database.models import HealthArticleRecord
from app.database.session import SessionLocal, normalize_db_value
from app.dto.health import HealthArticleDTO, HealthSourceDTO
from app.models.health_article import HealthArticle


class HealthRepository:
    _STOP_WORDS = {
        "alors", "au", "aucun", "aucune", "aussi", "autre", "aux", "avec", "avoir", "bon",
        "car", "ce", "cela", "ces", "comme", "comment", "dans", "de", "des", "du", "elle",
        "en", "et", "eux", "faire", "il", "ils", "je", "la", "le", "les", "leur", "lui",
        "ma", "mais", "me", "meme", "mes", "moi", "mon", "ne", "nos", "notre", "nous",
        "on", "ou", "par", "pas", "pour", "quand", "que", "quel", "quelle", "quels",
        "qui", "sa", "sans", "se", "ses", "son", "sous", "sur", "ta", "te", "tes", "toi",
        "ton", "tout", "tous", "tu", "un", "une", "vos", "votre", "vous", "y",
    }
    _CONCEPTS = {
        "hydratation": {"bois", "boire", "eau", "deshydrate", "deshydratation", "hydrate", "hydratation"},
        "sommeil": {"dors", "dormir", "dort", "endormir", "insomnie", "repos", "sommeil"},
        "chaleur": {"chaud", "chaude", "chaleur"},
    }

    def __init__(self, articles: list[HealthArticle] | None = None) -> None:
        self.articles = list(articles or [])

    @classmethod
    def _search_terms(cls, text: str) -> set[str]:
        normalized = unicodedata.normalize("NFKD", text.casefold())
        ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
        return {
            token
            for token in re.findall(r"[a-z0-9]+", ascii_text)
            if len(token) > 1 and token not in cls._STOP_WORDS
        }

    @classmethod
    def _search_concepts(cls, text: str) -> set[str]:
        terms = cls._search_terms(text)
        concepts = {alias: concept for concept, aliases in cls._CONCEPTS.items() for alias in aliases}
        return {concepts.get(term, term) for term in terms}

    @classmethod
    def _search_score(cls, query: str, article: HealthArticleDTO) -> int:
        query_concepts = cls._search_concepts(query)
        article_text = f"{article.title} {article.category} {article.content}"
        matching_concepts = query_concepts & cls._search_concepts(article_text)
        minimum_matches = max(1, math.ceil(len(query_concepts) * 0.25))
        return len(matching_concepts) if len(matching_concepts) >= minimum_matches else 0

    @staticmethod
    def _dto_from_model(article: HealthArticle) -> HealthArticleDTO:
        return HealthArticleDTO(
            article_id=article.article_id,
            title=article.title,
            category=article.category,
            content=article.content,
            country=article.country,
            language=article.language,
            source_name=article.source_name,
            source_url=article.source_url,
            publication_date=article.publication_date,
            last_verified=article.last_verified,
            reviewer=article.reviewer,
            status=article.status,
            version=article.version,
            next_revision=article.next_revision,
            is_demo=article.is_demo,
            notes=list(article.notes),
        )

    @staticmethod
    def _dto_from_record(row: HealthArticleRecord) -> HealthArticleDTO:
        return HealthArticleDTO(
            article_id=row.article_id,
            title=row.title,
            category=row.category,
            content=row.content,
            country=row.country,
            language=row.language,
            source_name=row.source_name,
            source_url=row.source_url,
            publication_date=row.publication_date,
            last_verified=row.last_verified,
            reviewer=row.reviewer,
            status=row.status,
            version=row.version,
            next_revision=row.next_revision,
            is_demo=row.is_demo,
            notes=list(row.notes or []),
        )

    @staticmethod
    def _matches_country(article: HealthArticleDTO, country: str) -> bool:
        normalized_country = normalize_country(country)
        return normalized_country == "ALL" or article.country == normalized_country or article.country == "ALL"

    @staticmethod
    def _matches_language(article: HealthArticleDTO, language: str) -> bool:
        normalized_language = normalize_language(language)
        article_base = article.language.split("-")[0].lower()
        requested_base = normalized_language.split("-")[0]
        return article.language.lower() == normalized_language or article_base == requested_base

    @staticmethod
    def _safe_article_payload(article: HealthArticleDTO) -> dict:
        return {
            "article_id": normalize_db_value(article.article_id, max_length=128),
            "title": normalize_db_value(article.title, max_length=200),
            "category": normalize_db_value(article.category, max_length=120),
            "content": normalize_db_value(article.content, max_length=8000),
            "country": normalize_db_value(article.country, max_length=2),
            "language": normalize_db_value(article.language, max_length=20),
            "source_name": normalize_db_value(article.source_name, max_length=200),
            "source_url": normalize_db_value(article.source_url, max_length=500) if article.source_url else None,
            "publication_date": article.publication_date,
            "last_verified": article.last_verified,
            "reviewer": normalize_db_value(article.reviewer, max_length=120) if article.reviewer else None,
            "status": normalize_db_value(article.status, max_length=50),
            "version": normalize_db_value(article.version, max_length=50),
            "next_revision": article.next_revision,
            "is_demo": bool(article.is_demo),
            "notes": [normalize_db_value(item, max_length=200) for item in (article.notes or [])],
        }

    def _save_article_to_db(self, article: HealthArticle | HealthArticleDTO) -> None:
        dto = self._dto_from_model(article) if isinstance(article, HealthArticle) else article
        payload = self._safe_article_payload(dto)
        db = SessionLocal()
        try:
            record = db.get(HealthArticleRecord, payload["article_id"])
            if record is None:
                db.add(HealthArticleRecord(**payload))
            else:
                for key, value in payload.items():
                    if key != "article_id":
                        setattr(record, key, value)
            db.commit()
        finally:
            db.close()

    def seed_default(self) -> None:
        for article in self.articles:
            self._save_article_to_db(article)

    def search(self, query: str, *, country: str = "SN", language: str = "fr") -> list[HealthArticleDTO]:
        cleaned_query = sanitize_text(query)
        if not cleaned_query:
            return []

        db = SessionLocal()
        try:
            rows = db.query(HealthArticleRecord).all()
        finally:
            db.close()

        results: list[HealthArticleDTO] = []
        for row in rows:
            article = self._dto_from_record(row)
            if self._matches_country(article, country) and self._matches_language(article, language):
                if self._search_score(cleaned_query, article):
                    results.append(article)
        if results:
            return sorted(
                results,
                key=lambda article: self._search_score(cleaned_query, article),
                reverse=True,
            )

        fallback_results = []
        for article in self.articles:
            dto = self._dto_from_model(article)
            if (
                self._matches_country(dto, country)
                and self._matches_language(dto, language)
                and self._search_score(cleaned_query, dto)
            ):
                fallback_results.append(dto)
        return sorted(
            fallback_results,
            key=lambda article: self._search_score(cleaned_query, article),
            reverse=True,
        )

    def get_all(self) -> list[HealthArticleDTO]:
        db = SessionLocal()
        try:
            rows = db.query(HealthArticleRecord).all()
        finally:
            db.close()
        if rows:
            return [self._dto_from_record(row) for row in rows]
        return [self._dto_from_model(article) for article in self.articles]

    def list_sources(self, *, country: str = "SN", language: str = "fr") -> list[HealthSourceDTO]:
        seen: set[str] = set()
        sources: list[HealthSourceDTO] = []
        for article in self.get_all():
            if not self._matches_country(article, country) or not self._matches_language(article, language):
                continue
            key = article.source_name.lower()
            if key in seen:
                continue
            seen.add(key)
            sources.append(
                HealthSourceDTO(
                    source_id=article.article_id,
                    name=article.source_name,
                    country=article.country,
                    language=article.language,
                    url=article.source_url,
                    last_verified=article.last_verified.isoformat() if article.last_verified else None,
                )
            )
        return sources
