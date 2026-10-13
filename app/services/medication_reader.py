from __future__ import annotations

from app.core.security import sanitize_text


class MedicationReader:
    def recognize(self, *, file_name: str, content_type: str, size_bytes: int) -> dict:
        normalized_name = sanitize_text(file_name)
        if not normalized_name.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            raise ValueError("Le fichier ne semble pas avoir un format d'image pris en charge.")
        if content_type not in {"image/jpeg", "image/png", "image/webp"}:
            raise ValueError("Le format du document est refusé pour l'OCR du prototype.")
        if size_bytes <= 0:
            raise ValueError("L'image est vide ou incomplète.")
        return {
            "status": "ambiguous",
            "candidates": [
                {
                    "candidate_id": "demo-01",
                    "display_name": "Médicament A (fiction)",
                    "confidence": 0.62,
                    "notes": "Image trop partielle pour confirmer une identité fiable.",
                },
                {
                    "candidate_id": "demo-02",
                    "display_name": "Médicament B (fiction)",
                    "confidence": 0.41,
                    "notes": "Plusieurs emballages similaires détectés, vérification requise.",
                },
            ],
            "requires_confirmation": True,
            "message": "Les éléments extraits sont non définitifs et doivent être confirmés par l'utilisateur avant toute recherche de notice.",
        }

    def confirm_candidate(self, *, candidate_id: str, confirmed: bool = True, question: str = "") -> dict:
        cleaned_candidate_id = sanitize_text(candidate_id)
        cleaned_question = sanitize_text(question)
        if not cleaned_candidate_id:
            raise ValueError("La référence du médicament est manquante.")
        if not confirmed:
            return {
                "status": "needs_review",
                "matched_source": None,
                "message": "Vérification requise. Le système ne peut pas identifier le médicament avec certitude.",
                "warnings": ["Aucune notice n'a été consultée sans confirmation utilisateur."],
            }
        if cleaned_question and "dosage" in cleaned_question.lower():
            return {
                "status": "verified_demo",
                "matched_source": "Notice de démonstration fictive — à remplacer par une notice officielle validée.",
                "message": "Le candidat a été retenu pour une recherche de démonstration seulement. Le dosage doit être vérifié avec la notice du fabricant ou un professionnel de santé.",
                "warnings": ["Ce résultat est démonstratif et non médicalement fiable."],
            }
        return {
            "status": "verified_demo",
            "matched_source": "Notice de démonstration fictive — à remplacer par une notice officielle validée.",
            "message": "Le candidat a été retenu pour une recherche de démonstration seulement. La notice réelle doit être vérifiée dans une source officielle.",
            "warnings": ["Ce résultat est démonstratif et non médicalement fiable."],
        }
