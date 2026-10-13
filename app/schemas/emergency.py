from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.security import normalize_country, normalize_language, sanitize_text


class EmergencySessionRequest(BaseModel):
    country: str = Field(default="SN", min_length=2, max_length=2, description="Code pays ISO du contexte d'urgence.")
    language: str = Field(default="fr", description="Langue de dialogue pour le parcours d'urgence.")
    scenario: str | None = Field(default=None, description="Scénario optionnel de démonstration.")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "country": "SN",
                "language": "fr",
                "scenario": "Patient avec douleur abdominale intense et faiblesse",
            }
        }
    )

    @field_validator("country")
    @classmethod
    def validate_country(cls, value: str) -> str:
        return normalize_country(value)

    @field_validator("language")
    @classmethod
    def validate_language(cls, value: str) -> str:
        return normalize_language(value)

    @field_validator("scenario")
    @classmethod
    def validate_scenario(cls, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = sanitize_text(value)
        if not cleaned:
            raise ValueError("Le scénario ne peut pas être vide.")
        return cleaned


class EmergencyAnswerRequest(BaseModel):
    answer: str = Field(..., min_length=1, max_length=200, description="Réponse de l'utilisateur au questionnaire d'urgence.")

    model_config = ConfigDict(
        json_schema_extra={"example": {"answer": "Oui, la douleur est intense et s'aggrave."}}
    )

    @field_validator("answer")
    @classmethod
    def validate_answer(cls, value: str) -> str:
        cleaned = sanitize_text(value)
        if not cleaned:
            raise ValueError("La réponse ne peut pas être vide.")
        return cleaned


class EmergencyProtocolOut(BaseModel):
    protocol_id: str = Field(..., description="Identifiant du protocole d'urgence.")
    title: str = Field(..., description="Titre du protocole de démonstration.")
    summary: str = Field(..., description="Résumé rapide du protocole.")
    country: str = Field(..., description="Pays cible du protocole.")
    version: str = Field(..., description="Version du protocole.")
    is_active: bool = Field(..., description="Indique si le protocole est actuellement activé.")
    is_demo: bool = Field(..., description="Indique qu'il s'agit d'un protocole de démonstration.")


class EmergencySessionResponse(BaseModel):
    session_id: str = Field(..., description="Identifiant de la session créée.")
    status: str = Field(..., description="Statut de progression de la session.")
    step: str = Field(..., description="Étape actuelle du parcours.")
    next_question: str | None = Field(default=None, description="Prochaine question du questionnaire.")
    guidance: str | None = Field(default=None, description="Conseil ou guidance associé à l'étape.")
    is_demo: bool = Field(default=True, description="Indique si la session est un prototype de démonstration.")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "session_id": "demo-session-001",
                "status": "in_progress",
                "step": "triage",
                "next_question": "Y a-t-il une douleur intense ou une perte de connaissance ?",
                "guidance": "Restez calme et contactez les services d'urgence si la situation s'aggrave.",
                "is_demo": True,
            }
        }
    )
