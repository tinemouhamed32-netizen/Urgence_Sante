from __future__ import annotations

from typing import Any

from fastapi import UploadFile

from app.core.config import ALLOWED_IMAGE_TYPES, MAX_UPLOAD_SIZE, SUPPORTED_LANGUAGES


def sanitize_text(value: str | None) -> str:
    if value is None:
        return ""
    cleaned = value.strip()
    return "".join(ch for ch in cleaned if ch.isprintable() and ch not in {"\x00"})


def normalize_country(value: str | None) -> str:
    normalized = (value or "SN").strip().upper()
    if len(normalized) != 2 or not normalized.isalpha():
        raise ValueError("Le code pays doit contenir exactement 2 lettres.")
    return normalized


def normalize_language(value: str | None) -> str:
    normalized = (value or "fr").strip().replace("_", "-").lower()
    if not normalized:
        return "fr"
    base = normalized.split("-")[0]
    if normalized in SUPPORTED_LANGUAGES or base in {option.split("-")[0] for option in SUPPORTED_LANGUAGES}:
        return normalized if normalized in SUPPORTED_LANGUAGES else base
    raise ValueError("La langue demandée n'est pas prise en charge par ce prototype.")


def validate_upload(file: UploadFile | None, *, max_size: int = MAX_UPLOAD_SIZE) -> None:
    if file is None:
        raise ValueError("Aucun fichier n'a été fourni.")
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise ValueError("Format de fichier non pris en charge. Utilisez JPEG, PNG ou WEBP.")
    if file.size is not None and file.size > max_size:
        raise ValueError("Le fichier est trop volumineux pour un traitement local de démonstration.")


def require_authorized_admin(user_role: str | None) -> None:
    if user_role != "admin":
        raise PermissionError("Accès non autorisé. Cette action nécessite un rôle administrateur.")


def redact_sensitive_value(value: str | None, *, keep_last: int = 4) -> str:
    if not value:
        return "***"
    if len(value) <= keep_last:
        return "*" * len(value)
    return "*" * (len(value) - keep_last) + value[-keep_last:]


def safe_dict(data: dict[str, Any]) -> dict[str, Any]:
    return {str(key): value for key, value in data.items()}
