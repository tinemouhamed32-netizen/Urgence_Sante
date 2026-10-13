from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


@dataclass(slots=True)
class HealthArticle:
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
