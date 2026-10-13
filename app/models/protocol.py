from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(slots=True)
class EmergencyProtocol:
    protocol_id: str
    title: str
    summary: str
    country: str
    version: str
    last_verified: date | None
    is_active: bool = True
    is_demo: bool = True
