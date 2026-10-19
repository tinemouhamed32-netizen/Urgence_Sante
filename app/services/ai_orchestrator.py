from __future__ import annotations

import re
import unicodedata

from app.core.security import normalize_country, normalize_language, sanitize_text
from app.services.emergency_engine import EmergencyEngine
from app.services.health_knowledge_base import HealthKnowledgeBase


class AIOrchestrator:
    _UNCONSCIOUSNESS_PHRASES = (
        "inconscient",
        "inconsciente",
        "inconscience",
        "ne repond pas",
        "ne se reveille pas",
        "perdu connaissance",
        "perte de connaissance",
        "evanoui",
        "evanouie",
    )
    _UNCONSCIOUSNESS_SOURCES = [
        "St John Ambulance — CPR | https://www.sja.org.uk/first-aid-advice/cpr/",
        "St John Ambulance — Position latérale de sécurité | https://www.sja.org.uk/first-aid-advice/recovery-position/",
        "SAMU National Sénégal — Contact | https://samu.sn/contact/",
    ]

    def __init__(self) -> None:
        self.emergency_engine = EmergencyEngine()
        self.knowledge_base = HealthKnowledgeBase()

    @staticmethod
    def _normalize_for_matching(text: str) -> str:
        normalized = unicodedata.normalize("NFKD", text.casefold())
        ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
        return re.sub(r"\s+", " ", ascii_text)

    @classmethod
    def _describes_unconsciousness(cls, question: str) -> bool:
        normalized = cls._normalize_for_matching(question)
        return any(phrase in normalized for phrase in cls._UNCONSCIOUSNESS_PHRASES)

    def classify_question(self, question: str) -> str:
        lowered = self._normalize_for_matching(sanitize_text(question))
        if any(
            word in lowered
            for word in [
                "saignement", "etouffement", "inconscient", "urgence", "douleur thoracique",
                "ne repond pas", "ne se reveille pas", "perdu connaissance", "perte de connaissance",
                "evanoui", "evanouie",
            ]
        ):
            return "emergency"
        if any(word in lowered for word in ["médicament", "pilule", "boîte", "notice", "dosage"]):
            return "medication"
        if any(
            word in lowered
            for word in [
                "nutrition", "sommeil", "dormir", "hydratation", "hydrater", "eau", "boire",
                "chaleur", "alimentation", "prévention",
            ]
        ):
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
            if self._describes_unconsciousness(cleaned_question):
                return {
                    "category": "emergency",
                    "answer": (
                        "Une personne inconsciente doit être considérée comme une urgence. "
                        "1. Vérifie que tu peux t'approcher sans danger. "
                        "2. Appelle immédiatement le SAMU/les secours locaux; demande à une personne précise "
                        "d'appeler et de chercher un défibrillateur, si disponible. Mets le téléphone en haut-parleur. "
                        "3. Vérifie si la personne répond et si elle respire normalement. Des halètements isolés "
                        "ne sont pas une respiration normale. "
                        "4. Si elle ne respire pas normalement, dis-le au régulateur et suis immédiatement ses "
                        "instructions; commence la réanimation si tu es formé et utilise un défibrillateur s'il est "
                        "disponible. "
                        "5. Si elle respire normalement, surveille sa respiration en attendant les secours. "
                        "Si aucune blessure au cou ou au dos n'est suspectée, place-la en position latérale de sécurité. "
                        "En cas de chute ou de traumatisme possible, évite de la déplacer sauf danger immédiat, "
                        "et suis les consignes des secours. Ne lui donne ni boisson ni nourriture et ne la laisse pas seule. "
                        "Au Sénégal, contacte le SAMU National; si tu ne connais pas son numéro, demande immédiatement "
                        "à un proche, à un agent de santé ou aux services locaux de t'aider à joindre les secours."
                    ),
                    "sources": self._UNCONSCIOUSNESS_SOURCES,
                    "limitations": [
                        "Ces gestes sont des premiers secours généraux et ne remplacent pas les instructions du régulateur.",
                        "N'attends pas une réponse de l'application pour appeler les secours.",
                    ],
                }
            return {
                "category": "emergency",
                "answer": (
                    "Cela peut être une urgence. Appelle immédiatement le SAMU/les secours locaux ou rends-toi "
                    "au service d'urgence le plus proche. Cette application ne peut pas évaluer une situation réelle "
                    "et ne doit pas retarder l'appel aux secours."
                ),
                "sources": [],
                "limitations": ["Cette réponse ne constitue pas un diagnostic ni un triage médical."],
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
            "limitations": [
                "La réponse provient d'une fiche de démonstration non référencée et non vérifiée pour un usage médical.",
                "Ce n'est pas un avis médical personnalisé.",
            ],
        }
