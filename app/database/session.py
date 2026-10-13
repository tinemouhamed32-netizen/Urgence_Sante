from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from app.core.security import sanitize_text
from app.database.base import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./urgence_sante.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def normalize_db_value(value: str | None, *, max_length: int | None = None, allow_blank: bool = False) -> str | None:
    if value is None:
        return None
    cleaned = sanitize_text(str(value))
    if not cleaned and not allow_blank:
        raise ValueError("La valeur de base de données ne peut pas être vide.")
    if max_length is not None and len(cleaned) > max_length:
        raise ValueError(f"La valeur de base de données dépasse la taille maximale autorisée ({max_length} caractères).")
    return cleaned


@event.listens_for(engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record) -> None:  # type: ignore[no-untyped-def]
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA busy_timeout = 5000")
    cursor.close()


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
