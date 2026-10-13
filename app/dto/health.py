from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


@dataclass(slots=True)
class HealthArticleDTO:
    article_id: str
    title: str
    category: str
    content: str
    country: str
    language: str
    source_name: str
    source_url: str | None = None
    publication_date: date | None = None
    last_verified: date | None = None
    reviewer: str | None = None
    status: str = "validated"
    version: str = "1.0"
    next_revision: date | None = None
    is_demo: bool = True
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "article_id": self.article_id,
            "title": self.title,
            "category": self.category,
            "content": self.content,
            "country": self.country,
            "language": self.language,
            "source_name": self.source_name,
            "source_url": self.source_url,
            "publication_date": self.publication_date.isoformat() if self.publication_date else None,
            "last_verified": self.last_verified.isoformat() if self.last_verified else None,
            "reviewer": self.reviewer,
            "status": self.status,
            "version": self.version,
            "next_revision": self.next_revision.isoformat() if self.next_revision else None,
            "is_demo": self.is_demo,
            "notes": list(self.notes),
        }


@dataclass(slots=True)
class HealthSourceDTO:
    source_id: str
    name: str
    country: str
    language: str
    url: str | None
    last_verified: str | None

    def to_dict(self) -> dict:
        return {
            "source_id": self.source_id,
            "name": self.name,
            "country": self.country,
            "language": self.language,
            "url": self.url,
            "last_verified": self.last_verified,
        }
