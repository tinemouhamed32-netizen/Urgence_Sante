from __future__ import annotations

import json
from pathlib import Path


def export_signed_payload(payload: dict, *, destination: str | Path) -> str:
    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(path)
