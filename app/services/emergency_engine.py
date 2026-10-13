from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4

from app.core.security import normalize_country, normalize_language, sanitize_text
from app.database.session import init_db
from app.dto.emergency import EmergencySessionDTO
from app.models.protocol import EmergencyProtocol
from app.repositories.emergency_session_repository import EmergencySessionRepository


@dataclass
class EmergencySession:
    session_id: str
    status: str
    step: str
    next_question: str | None = None
    guidance: str | None = None
    is_demo: bool = True
    answers: dict[str, str] = field(default_factory=dict)


class EmergencyEngine:
    """Deterministic emergency workflow used for demonstration only."""

    def __init__(self) -> None:
        init_db()
        self.repository = EmergencySessionRepository()
        self.protocols = [
            EmergencyProtocol(
                protocol_id="demo-severe-bleeding",
                title="Hémorragie grave (démonstration)",
                summary="Simulation d'un saignement important avec signe d'urgence",
                country="SN",
                version="0.1-demo",
                last_verified=None,
                is_active=True,
                is_demo=True,
            )
        ]
        self._sessions: dict[str, EmergencySession] = {}

    def _persist_session(self, session: EmergencySession) -> None:
        dto = EmergencySessionDTO(
            session_id=session.session_id,
            status=session.status,
            step=session.step,
            next_question=session.next_question,
            guidance=session.guidance,
            is_demo=session.is_demo,
            answers={str(key): str(value) for key, value in session.answers.items()},
            country=session.answers.get("country", "SN"),
            language=session.answers.get("language", "fr"),
            scenario=session.answers.get("scenario"),
        )
        self.repository.save(dto)

    def list_protocols(self) -> list[EmergencyProtocol]:
        return list(self.protocols)

    def get_session(self, session_id: str) -> EmergencySession | None:
        session = self._sessions.get(session_id)
        if session is not None:
            return session
        dto = self.repository.get_by_id(session_id)
        if dto is None:
            return None
        return EmergencySession(
            session_id=dto.session_id,
            status=dto.status,
            step=dto.step,
            next_question=dto.next_question,
            guidance=dto.guidance,
            is_demo=dto.is_demo,
            answers=dict(dto.answers),
        )

    def start_session(self, *, country: str = "SN", language: str = "fr", scenario: str | None = None) -> EmergencySession:
        normalized_country = normalize_country(country)
        normalized_language = normalize_language(language)
        sanitized_scenario = sanitize_text(scenario) if scenario is not None else None
        session_id = f"demo-{uuid4().hex[:8]}"
        session = EmergencySession(
            session_id=session_id,
            status="in_progress",
            step="triage",
            next_question="Y a-t-il une hémorragie visible ou un état de conscience altéré ?",
            guidance="Ce parcours est une démonstration fictive et ne remplace pas un professionnel de santé.",
            is_demo=True,
        )
        if sanitized_scenario:
            session.answers["scenario"] = sanitized_scenario
            session.guidance = f"Scenario: {sanitized_scenario}. {session.guidance}"
        session.answers["country"] = normalized_country
        session.answers["language"] = normalized_language
        self._sessions[session_id] = session
        self._persist_session(session)
        return session

    def answer(self, session: EmergencySession, answer: str) -> EmergencySession:
        normalized = sanitize_text(answer).lower()
        session.answers[session.step] = normalized
        if normalized in {"oui", "yes", "y"} and session.step == "triage":
            session.step = "immediate_alert"
            session.status = "requires_immediate_help"
            session.next_question = None
            session.guidance = "Contactez immédiatement les secours et poursuivez les gestes de base selon le protocole validé disponible hors ligne."
            self._persist_session(session)
            return session
        if normalized in {"non", "no", "n"} and session.step == "triage":
            session.step = "monitoring"
            session.status = "monitoring"
            session.next_question = "Le patient est-il stable et conscient ?"
            session.guidance = "Continuer la surveillance et demander une évaluation médicale si le symptôme persiste."
            self._persist_session(session)
            return session
        if session.step == "immediate_alert":
            session.status = "resolved"
            session.next_question = None
            session.guidance = "Alerte immédiate. Ce scénario ne remplace pas l'avis d'un professionnel."
            self._persist_session(session)
            return session
        if session.step == "monitoring":
            session.status = "resolved"
            session.next_question = None
            session.guidance = "Le cas est surveillé. Si la situation évolue, contactez un professionnel de santé."
            self._persist_session(session)
            return session
        session.status = "resolved"
        session.guidance = "Réponse enregistrée. Ce moteur est une démonstration fictive."
        self._persist_session(session)
        return session
