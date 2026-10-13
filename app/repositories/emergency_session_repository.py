from __future__ import annotations

from app.database.models import EmergencySessionRecord
from app.database.session import SessionLocal, normalize_db_value
from app.dto.emergency import EmergencySessionDTO


class EmergencySessionRepository:
    def save(self, session: EmergencySessionDTO) -> None:
        payload = {
            "session_id": normalize_db_value(session.session_id, max_length=128),
            "status": normalize_db_value(session.status, max_length=50),
            "step": normalize_db_value(session.step, max_length=50),
            "next_question": normalize_db_value(session.next_question, max_length=300) if session.next_question else None,
            "guidance": normalize_db_value(session.guidance, max_length=800) if session.guidance else None,
            "is_demo": bool(session.is_demo),
            "country": normalize_db_value(session.country, max_length=2),
            "language": normalize_db_value(session.language, max_length=20),
            "scenario": normalize_db_value(session.scenario, max_length=300) if session.scenario else None,
            "answers": {str(key): str(value) for key, value in session.answers.items()},
        }

        db = SessionLocal()
        try:
            record = db.get(EmergencySessionRecord, payload["session_id"])
            if record is None:
                db.add(EmergencySessionRecord(**payload))
            else:
                for key, value in payload.items():
                    if key != "session_id":
                        setattr(record, key, value)
            db.commit()
        finally:
            db.close()

    def get_by_id(self, session_id: str) -> EmergencySessionDTO | None:
        db = SessionLocal()
        try:
            record = db.get(EmergencySessionRecord, session_id)
        finally:
            db.close()
        if record is None:
            return None
        return EmergencySessionDTO(
            session_id=record.session_id,
            status=record.status,
            step=record.step,
            next_question=record.next_question,
            guidance=record.guidance,
            is_demo=record.is_demo,
            answers={str(key): str(value) for key, value in (record.answers or {}).items()},
            country=record.country,
            language=record.language,
            scenario=record.scenario,
        )
