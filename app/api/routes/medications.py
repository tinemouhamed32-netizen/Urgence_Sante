from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.schemas.common import ErrorResponse
from app.schemas.medication import MedicationConfirmationRequest, MedicationImageRequest, MedicationRecognitionResponse, MedicationVerificationResponse
from app.services.medication_reader import MedicationReader

router = APIRouter(prefix="/api/v1/medications", tags=["medications"])
reader = MedicationReader()


@router.post(
    "/recognize",
    response_model=MedicationRecognitionResponse,
    summary="Reconnaît une image de médicament",
    description="Simule une reconnaissance OCR d'image de médicament dans un contexte de démonstration et retourne des candidats à validation.",
    responses={
        200: {"description": "Candidats de reconnaissance retournés avec succès."},
        400: {"model": ErrorResponse, "description": "Le payload image est invalide ou incomplet."},
    },
)
def recognize_medication(payload: MedicationImageRequest) -> MedicationRecognitionResponse:
    try:
        result = reader.recognize(file_name=payload.file_name, content_type=payload.content_type, size_bytes=payload.size_bytes)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return MedicationRecognitionResponse(**result)


@router.post(
    "/confirm",
    response_model=MedicationVerificationResponse,
    summary="Valide un candidat médicamenteux",
    description="Confirme ou rejette un candidat identifié à partir d'une image, en rappelant que le résultat est démonstratif et non médicalement fiable.",
    responses={
        200: {"description": "Validation du candidat retournée."},
        400: {"model": ErrorResponse, "description": "Le candidat ou la question de confirmation est invalide."},
    },
)
def confirm_medication(payload: MedicationConfirmationRequest) -> MedicationVerificationResponse:
    try:
        result = reader.confirm_candidate(
            candidate_id=payload.candidate_id,
            confirmed=payload.confirmed,
            question=payload.question,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return MedicationVerificationResponse(**result)
