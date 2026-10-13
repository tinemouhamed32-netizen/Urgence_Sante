from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class EmergencySessionDTO:
    session_id: str
    status: str
    step: str
    next_question: str | None = None
    guidance: str | None = None
    is_demo: bool = True
    answers: dict[str, str] = field(default_factory=dict)
    country: str = "SN"
    language: str = "fr"
    scenario: str | None = None

    def to_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "status": self.status,
            "step": self.step,
            "next_question": self.next_question,
            "guidance": self.guidance,
            "is_demo": self.is_demo,
            "answers": dict(self.answers),
            "country": self.country,
            "language": self.language,
            "scenario": self.scenario,
        }
