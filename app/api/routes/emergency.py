from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.schemas.common import ErrorResponse
from app.schemas.emergency import EmergencyAnswerRequest, EmergencyProtocolOut, EmergencySessionRequest, EmergencySessionResponse
from app.services.emergency_service import EmergencyService

router = APIRouter(prefix="/api/v1/emergency", tags=["emergency"])
emergency_service = EmergencyService()


@router.get(
    "/protocols",
    response_model=list[EmergencyProtocolOut],
    summary="Liste les protocoles d'urgence de démonstration",
    description="Renvoie les protocoles disponibles pour le parcours d'urgence du prototype.",
    responses={
        200: {"description": "Liste des protocoles disponibles."},
    },
)
def list_protocols() -> list[EmergencyProtocolOut]:
    protocols = emergency_service.list_protocols()
    return [
        EmergencyProtocolOut(
            protocol_id=protocol["protocol_id"],
            title=protocol["title"],
            summary=protocol["summary"],
            country=protocol["country"],
            version=protocol["version"],
            is_active=protocol["is_active"],
            is_demo=protocol["is_demo"],
        )
        for protocol in protocols
    ]


@router.post(
    "/session",
    response_model=EmergencySessionResponse,
    summary="Démarre une session d'urgence de démonstration",
    description="Crée une session avec un contexte pays/langue et un scénario optionnel, utilisé pour le parcours de démonstration.",
    responses={
        200: {"description": "Session initialisée avec le premier questionnaire."},
        400: {"model": ErrorResponse, "description": "Le contexte ou le scénario est invalide."},
    },
)
def start_session(payload: EmergencySessionRequest) -> EmergencySessionResponse:
    try:
        session = emergency_service.start_session(country=payload.country, language=payload.language, scenario=payload.scenario)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return EmergencySessionResponse(
        session_id=session.session_id,
        status=session.status,
        step=session.step,
        next_question=session.next_question,
        guidance=session.guidance,
        is_demo=session.is_demo,
    )


@router.post(
    "/session/{session_id}/answer",
    response_model=EmergencySessionResponse,
    summary="Envoie une réponse dans une session d'urgence",
    description="Met à jour l'état de la session suivant la réponse fournie par l'utilisateur.",
    responses={
        200: {"description": "La session a été mise à jour."},
        400: {"model": ErrorResponse, "description": "Le contenu de la réponse est invalide."},
        404: {"model": ErrorResponse, "description": "La session demandée n'existe pas."},
    },
)
def answer_session(session_id: str, payload: EmergencyAnswerRequest) -> EmergencySessionResponse:
    try:
        updated = emergency_service.answer_session(session_id, payload.answer)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return EmergencySessionResponse(
        session_id=updated.session_id,
        status=updated.status,
        step=updated.step,
        next_question=updated.next_question,
        guidance=updated.guidance,
        is_demo=updated.is_demo,
    )
