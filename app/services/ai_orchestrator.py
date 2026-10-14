from __future__ import annotations

from app.core.security import normalize_country, normalize_language, sanitize_text
from app.services.emergency_engine import EmergencyEngine
from app.services.health_knowledge_base import HealthKnowledgeBase


class AIOrchestrator:
    def __init__(self) -> None:
        self.emergency_engine = EmergencyEngine()
        self.knowledge_base = HealthKnowledgeBase()

    def classify_question(self, question: str) -> str:
        lowered = sanitize_text(question).casefold()
        if any(word in lowered for word in ["saignement", "étouffement", "inconscient", "urgence", "douleur thoracique"]):
            return "emergency"
        if any(word in lowered for word in ["médicament", "pilule", "boîte", "notice", "dosage"]):
            return "medication"
        if any(word in lowered for word in ["nutrition", "sommeil", "hydratation", "alimentation", "prévention"]):
            return "general"
        return "out_of_scope"

    def answer_question(self, question: str, *, country: str = "SN", language: str = "fr") -> dict:
        cleaned_question = sanitize_text(question)
        if not cleaned_question:
            raise ValueError("La question ne peut pas être vide.")

        normalized_country = normalize_country(country)
        normalized_language = normalize_language(language)
        category = self.classify_question(cleaned_question)
        if category == "emergency":
            session = self.emergency_engine.start_session(country=normalized_country, language=normalized_language)
            return {
                "category": "emergency",
                "answer": "Cette démonstration ne réalise pas de triage médical. En cas de situation réelle, contactez immédiatement les services de secours locaux.",
                "sources": ["Protocoles de démonstration fictifs"],
                "limitations": ["Ce n'est pas un diagnostic médical et les données sont fictives."],
                "session": {
                    "session_id": session.session_id,
                    "next_question": session.next_question,
                },
            }

        docs = self.knowledge_base.search(cleaned_question, country=normalized_country, language=normalized_language)
        if not docs:
            return {
                "category": category,
                "answer": "Aucune information vérifiée n'a été trouvée dans le corpus de démonstration pour cette demande.",
                "sources": [],
                "limitations": ["Le système demande une vérification professionnelle si la réponse est incertaine."],
            }

        answer = docs[0]["content"]
        return {
            "category": category,
            "answer": answer,
            "sources": [doc["source"] for doc in docs],
            "limitations": ["La réponse est une synthèse du corpus vérifié, pas un avis médical personnalisé."],
        }
