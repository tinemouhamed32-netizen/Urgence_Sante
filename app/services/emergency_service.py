from __future__ import annotations

from app.core.security import normalize_country, normalize_language, sanitize_text
from app.services.emergency_engine import EmergencyEngine, EmergencySession


class EmergencyService:
    def __init__(self, engine: EmergencyEngine | None = None) -> None:
        self.engine = engine or EmergencyEngine()

    def list_protocols(self) -> list[dict]:
        return [
            {
                "protocol_id": protocol.protocol_id,
                "title": protocol.title,
                "summary": protocol.summary,
                "country": protocol.country,
                "version": protocol.version,
                "is_active": protocol.is_active,
                "is_demo": protocol.is_demo,
            }
            for protocol in self.engine.list_protocols()
        ]

    def start_session(self, *, country: str = "SN", language: str = "fr", scenario: str | None = None) -> EmergencySession:
        normalized_country = normalize_country(country)
        normalized_language = normalize_language(language)
        cleaned_scenario = sanitize_text(scenario) if scenario is not None else None
        return self.engine.start_session(country=normalized_country, language=normalized_language, scenario=cleaned_scenario)

    def answer_session(self, session_id: str, answer: str) -> EmergencySession:
        cleaned_session_id = sanitize_text(session_id)
        if not cleaned_session_id:
            raise ValueError("L'identifiant de la session est invalide.")

        session = self.engine.get_session(cleaned_session_id)
        if session is None:
            raise KeyError("Session introuvable dans ce prototype de démonstration.")
        return self.engine.answer(session, answer)
