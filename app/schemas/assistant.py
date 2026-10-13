from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.security import normalize_country, normalize_language, sanitize_text


class AssistantMessageRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000, description="Question formulée par l'utilisateur à l'assistant.")
    country: str = Field(default="SN", min_length=2, max_length=2, description="Code ISO du pays pour adapter la réponse.")
    language: str = Field(default="fr", description="Langue de réponse demandée par le client.")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "question": "J'ai de la fièvre et une toux sèche depuis 2 jours, que faire ?",
                "country": "SN",
                "language": "fr",
            }
        }
    )

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:
        cleaned = sanitize_text(value)
        if not cleaned:
            raise ValueError("La question ne peut pas être vide.")
        return cleaned

    @field_validator("country")
    @classmethod
    def validate_country(cls, value: str) -> str:
        return normalize_country(value)

    @field_validator("language")
    @classmethod
    def validate_language(cls, value: str) -> str:
        return normalize_language(value)


class AssistantMessageResponse(BaseModel):
    category: str = Field(..., description="Catégorie de réponse associée à la demande.")
    answer: str = Field(..., description="Réponse générale de démonstration proposée à l'utilisateur.")
    sources: list[str] = Field(..., description="Sources documentaires ou références de contexte utilisées pour la réponse.")
    limitations: list[str] = Field(..., description="Limites et précautions associées au prototype.")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "category": "prévention",
                "answer": "La fièvre et la toux peuvent correspondre à plusieurs causes...",
                "sources": ["OMS", "Ministère de la Santé"],
                "limitations": ["Réponse de démonstration", "Non remplace un avis médical"],
            }
        }
    )
