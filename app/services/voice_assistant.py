from __future__ import annotations


class VoiceAssistant:
    def supported_languages(self) -> list[str]:
        return ["fr", "fr-SN", "en", "wo"]

    def speak(self, text: str, *, volume: int = 80, speed: float = 1.0) -> dict:
        return {"status": "demo_only", "text": text, "volume": volume, "speed": speed}

    def transcribe(self, audio_content: bytes | None) -> dict:
        if not audio_content:
            return {"status": "needs_confirmation", "text": "Aucun audio valide reçu."}
        return {"status": "demo_only", "text": "Audio reçu en mode démonstration, non interprété médicalement."}
