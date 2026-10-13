from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class MedicationImageRequest(BaseModel):
    file_name: str = Field(..., min_length=1, max_length=255, description="Nom du fichier image à analyser.")
    content_type: str = Field(default="image/jpeg", description="Type MIME de l'image fournie par le client.")
    size_bytes: int = Field(default=0, ge=0, le=10_000_000, description="Taille du fichier image en octets.")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "file_name": "paracetamol.jpg",
                "content_type": "image/jpeg",
                "size_bytes": 245760,
            }
        }
    )


class MedicationCandidate(BaseModel):
    candidate_id: str = Field(..., description="Identifiant interne du candidat médicamenteux.")
    display_name: str = Field(..., description="Nom affiché du candidat identifié.")
    confidence: float = Field(..., description="Niveau de confiance de l'identification.")
    notes: str = Field(..., description="Note d'analyse associée au candidat.")


class MedicationConfirmationRequest(BaseModel):
    candidate_id: str = Field(..., min_length=1, description="Identifiant du candidat à confirmer.")
    confirmed: bool = Field(default=True, description="Indique si le candidat est confirmé par l'utilisateur.")
    question: str = Field(default="Le médicament affiché est-il bien reconnu ?", description="Question de validation envoyée au moteur.")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "candidate_id": "med-001",
                "confirmed": True,
                "question": "Le médicament affiché est-il bien reconnu ?",
            }
        }
    )


class MedicationRecognitionResponse(BaseModel):
    status: str = Field(..., description="Statut de la reconnaissance.")
    candidates: list[MedicationCandidate] = Field(..., description="Liste des candidats identifiés.")
    requires_confirmation: bool = Field(..., description="Indique si une validation manuelle est attendue.")
    message: str = Field(..., description="Message de contexte renvoyé au client.")


class MedicationVerificationResponse(BaseModel):
    status: str = Field(..., description="Statut final de la vérification.")
    matched_source: str | None = Field(default=None, description="Source ou référence correspondant au médicament vérifié.")
    message: str = Field(..., description="Message de vérification détaillé.")
    warnings: list[str] = Field(default_factory=list, description="Avertissements émis lors de la validation.")
