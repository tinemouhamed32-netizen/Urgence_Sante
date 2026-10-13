from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from sqlalchemy import JSON, Boolean, Column, Date, String, Text

from app.database.base import Base


class HealthArticleRecord(Base):
    __tablename__ = "health_articles"

    article_id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    country = Column(String, nullable=False, default="SN")
    language = Column(String, nullable=False, default="fr")
    source_name = Column(String, nullable=False)
    source_url = Column(String, nullable=True)
    publication_date = Column(Date, nullable=True)
    last_verified = Column(Date, nullable=True)
    reviewer = Column(String, nullable=True)
    status = Column(String, nullable=False, default="validated")
    version = Column(String, nullable=False, default="1.0")
    next_revision = Column(Date, nullable=True)
    is_demo = Column(Boolean, nullable=False, default=True)
    notes = Column(JSON, nullable=False, default=list)
    created_at = Column(String, nullable=False, default=lambda: datetime.now(timezone.utc).isoformat(timespec="seconds"))
    updated_at = Column(String, nullable=False, default=lambda: datetime.now(timezone.utc).isoformat(timespec="seconds"), onupdate=lambda: datetime.now(timezone.utc).isoformat(timespec="seconds"))


class EmergencySessionRecord(Base):
    __tablename__ = "emergency_sessions"

    session_id = Column(String, primary_key=True, index=True)
    status = Column(String, nullable=False, default="in_progress")
    step = Column(String, nullable=False, default="triage")
    next_question = Column(String, nullable=True)
    guidance = Column(String, nullable=True)
    is_demo = Column(Boolean, nullable=False, default=True)
    country = Column(String, nullable=False, default="SN")
    language = Column(String, nullable=False, default="fr")
    scenario = Column(String, nullable=True)
    answers = Column(JSON, nullable=False, default=dict)
    created_at = Column(String, nullable=False, default=lambda: datetime.now(timezone.utc).isoformat(timespec="seconds"))
    updated_at = Column(String, nullable=False, default=lambda: datetime.now(timezone.utc).isoformat(timespec="seconds"), onupdate=lambda: datetime.now(timezone.utc).isoformat(timespec="seconds"))


def json_safe(value: Any) -> list[str] | dict[str, str]:
    if isinstance(value, (list, dict)):
        return value
    if value is None:
        return [] if isinstance(value, list) else {}
    return value
