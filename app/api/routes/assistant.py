from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.schemas.assistant import AssistantMessageRequest, AssistantMessageResponse
from app.schemas.common import ErrorResponse
from app.services.ai_orchestrator import AIOrchestrator

router = APIRouter(prefix="/api/v1/assistant", tags=["assistant"])
assistant = AIOrchestrator()


@router.post(
    "/message",
    response_model=AssistantMessageResponse,
    summary="Pose une question générale à l'assistant de santé",
    description="Renvoie une réponse de démonstration, avec sources et limites, selon le contexte pays/langue et la question fournie.",
    responses={
        200: {"description": "Réponse de démonstration retournée."},
        400: {"model": ErrorResponse, "description": "Le payload est invalide ou la question est vide."},
    },
)
def answer_message(payload: AssistantMessageRequest) -> AssistantMessageResponse:
    try:
        result = assistant.answer_question(payload.question, country=payload.country, language=payload.language)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return AssistantMessageResponse(
        category=result["category"],
        answer=result["answer"],
        sources=result.get("sources", []),
        limitations=result.get("limitations", []),
    )
