from __future__ import annotations


class SpeechProvider:
    """Minimal speech adapter interface for local and cloud synthesis."""

    def synthesize(self, text: str, *, language: str = "fr") -> bytes:
        raise NotImplementedError("Aucune implémentation de synthèse vocale n'a encore été configurée.")

    def transcribe(self, audio_bytes: bytes) -> str:
        raise NotImplementedError("Aucune implémentation de transcription vocale n'a encore été configurée.")
