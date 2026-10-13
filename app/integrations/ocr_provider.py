from __future__ import annotations


class OCRProvider:
    """Minimal OCR adapter interface."""

    def extract_text(self, image_bytes: bytes) -> dict[str, object]:
        raise NotImplementedError("Aucune implémentation OCR n'a encore été configurée.")
