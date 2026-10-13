from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(slots=True)
class MedicalSource:
    source_id: str
    name: str
    country: str
    language: str
    url: str | None
    published_on: date | None
    last_checked: date
    status: str = "approved"
    is_official: bool = True
