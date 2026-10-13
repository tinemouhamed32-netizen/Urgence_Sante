from __future__ import annotations


class LLMProvider:
    """Minimal adapter interface for future AI provider integration."""

    def generate(self, prompt: str) -> str:
        raise NotImplementedError("Aucune implémentation de fournisseur LLM n'a encore été configurée.")
