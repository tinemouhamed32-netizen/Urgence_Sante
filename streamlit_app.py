from __future__ import annotations

import os
from typing import Any

import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")
if "://" not in BACKEND_URL:
    BACKEND_URL = f"https://{BACKEND_URL}"

st.set_page_config(page_title="Urgence Santé Demo", page_icon="⚕️", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at top left, rgba(72,118,255,0.20), transparent 28%),
                    linear-gradient(135deg, #060d16 0%, #0b1625 35%, #0b1220 100%);
        color: #edf3ff;
    }
    .block-container {
        padding-top: 1.6rem;
        padding-bottom: 3rem;
        max-width: 1440px;
    }
    .stSidebar {
        background: rgba(9, 17, 27, 0.94);
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    .stSidebar .block-container {
        padding-top: 1.5rem;
    }
    h1, h2, h3, h4 {
        color: #f8fbff;
    }
    .hero {
        font-size: clamp(3rem, 6vw, 6.2rem);
        line-height: 0.92;
        font-weight: 800;
        letter-spacing: -0.065em;
        color: #f3f7ff;
        margin: 0.3rem 0 1rem 0;
    }
    .subhero {
        font-size: clamp(1.1rem, 2vw, 1.5rem);
        color: #d8e3f6;
        opacity: 0.92;
        max-width: 1100px;
        line-height: 1.45;
    }
    .badge {
        display: inline-block;
        padding: 0.38rem 0.9rem;
        border-radius: 999px;
        background: rgba(130, 167, 255, 0.12);
        color: #b9ccff;
        border: 1px solid rgba(185, 204, 255, 0.28);
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }
    .panel {
        background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 1.15rem 1.2rem;
        box-shadow: 0 18px 48px rgba(4, 10, 18, 0.25);
    }
    .metric-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 1rem 1rem 0.9rem 1rem;
        min-height: 120px;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.04);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        line-height: 1;
        color: #f5f9ff;
    }
    .metric-label {
        font-size: 0.82rem;
        color: #b7c8e6;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin-top: 0.5rem;
    }
    .chip {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 0.3rem 0.8rem;
        border-radius: 999px;
        background: rgba(255, 125, 90, 0.12);
        color: #ffb39d;
        border: 1px solid rgba(255,179,157,0.25);
        font-weight: 700;
    }
    .reply-user {
        background: rgba(92, 122, 255, 0.18);
        border-left: 3px solid #8aa9ff;
        padding: 0.8rem 0.9rem;
        border-radius: 12px;
        margin-bottom: 0.6rem;
        color: #f2f6ff;
    }
    .reply-assistant {
        background: rgba(255,255,255,0.03);
        border-left: 3px solid #6dd9a7;
        padding: 0.8rem 0.9rem;
        border-radius: 12px;
        margin-bottom: 0.6rem;
        color: #edf7f2;
    }
    .searchbox {
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 0.5rem 0.8rem;
    }
    .kicker {
        display: inline-block;
        margin-bottom: 0.7rem;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 999px;
        padding: 0.35rem 0.75rem;
        color: #d6e3ff;
        font-size: 0.74rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "backend_ok" not in st.session_state:
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=3)
        st.session_state["backend_ok"] = response.status_code == 200
    except requests.RequestException:
        st.session_state["backend_ok"] = False

backend_ok = st.session_state["backend_ok"]

with st.sidebar:
    st.markdown("<div class='badge'>AI4Youth 2026</div>", unsafe_allow_html=True)
    st.title("Urgence Santé")
    st.caption("Prototype technique interactif")
    st.markdown("---")
    st.markdown(
        """
        - parcours d'urgence simulé
        - assistance générale de santé
        - reconnaissance de médicament (démo)
        - contrôle des sources et limites
        """
    )
    if backend_ok:
        st.success("Backend connecté")
    else:
        st.warning("Mode hors ligne simulé")
    st.caption("Données fictives et démonstratives")

st.markdown("<div class='kicker'>prototype IA santé</div>", unsafe_allow_html=True)
st.markdown("<div class='hero'>Urgence Santé —<br>prototype de démonstration</div>", unsafe_allow_html=True)
st.markdown("<div class='subhero'>Aide sanitaire guidée, sécurisée, informative et limitée à des usages de démonstration.</div>", unsafe_allow_html=True)

metric_cols = st.columns(3)
with metric_cols[0]:
    st.markdown("<div class='metric-card'><div class='metric-value'>24/7</div><div class='metric-label'>Disponibilité simulée</div></div>", unsafe_allow_html=True)
with metric_cols[1]:
    st.markdown("<div class='metric-card'><div class='metric-value'>3</div><div class='metric-label'>Modules clés</div></div>", unsafe_allow_html=True)
with metric_cols[2]:
    st.markdown("<div class='metric-card'><div class='metric-value'>100%</div><div class='metric-label'>Démonstration</div></div>", unsafe_allow_html=True)

st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def get_demo_sources() -> dict[str, Any]:
    return {
        "hydration": {
            "answer": "Boire régulièrement de l'eau et ajuster l'apport selon la chaleur et l'activité physique.",
            "sources": ["Ministère de la Santé du Sénégal", "OMS"],
            "limitations": ["Conseil général et non personnalisé.", "À utiliser avec prudence et avis professionnel selon le contexte."],
        },
        "urgent": {
            "answer": "Le système a détecté un scénario d'urgence. Un protocole prévalidé et hors ligne doit être appliqué.",
            "sources": ["Protocole de démonstration fictif"],
            "limitations": ["Aucune décision critique ne doit être laissée au modèle seul.", "Ce scénario ne remplace pas les secours ni un professionnel."],
        },
    }


def call_backend(path: str, *, method: str = "GET", payload: dict | None = None) -> Any:
    url = f"{BACKEND_URL}{path}"
    if method == "GET":
        response = requests.get(url, timeout=5)
    else:
        response = requests.post(url, json=payload, timeout=5)
    if response.status_code >= 400:
        raise RuntimeError(response.json().get("detail", response.text))
    return response.json()


def reset_emergency_session() -> None:
    st.session_state.pop("emergency_session_id", None)
    st.session_state.pop("emergency_step", None)
    st.session_state.pop("emergency_guidance", None)


if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [
        {"role": "assistant", "text": "Bonjour ! Je peux vous expliquer des conseils de prévention, aider à formuler une question de santé générale ou guider une simulation d'urgence fictive."}
    ]

chat_col, status_col = st.columns([2, 1])

with chat_col:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.markdown("<h3>Assistant de santé</h3>", unsafe_allow_html=True)

    for message in st.session_state["chat_history"]:
        role = message["role"]
        bubble_class = "reply-user" if role == "user" else "reply-assistant"
        label = "Vous" if role == "user" else "Assistant"
        st.markdown(f"<div class='{bubble_class}'><strong>{label}</strong><br>{message['text']}</div>", unsafe_allow_html=True)

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Votre message", placeholder="Posez une question de santé générale ...")
        submitted = st.form_submit_button("Envoyer")

    if submitted and user_input.strip():
        st.session_state["chat_history"].append({"role": "user", "text": user_input.strip()})
        if backend_ok:
            try:
                data = call_backend("/api/v1/assistant/message", method="POST", payload={"question": user_input.strip(), "country": "SN", "language": "fr"})
                reply = data.get("answer", "Aucune réponse disponible")
                sources = ", ".join(data.get("sources", [])) or "Aucune source listée"
                limitations = "; ".join(data.get("limitations", [])) or "Aucune limite particulière mentionnée"
                assistant_reply = f"{reply} \n\nSources : {sources} \nLimites : {limitations}"
            except RuntimeError:
                demo = get_demo_sources()["hydration"]
                assistant_reply = f"{demo['answer']}\n\nSources : {', '.join(demo['sources'])}\nLimites : {'; '.join(demo['limitations'])}"
        else:
            demo = get_demo_sources()["hydration"]
            assistant_reply = f"{demo['answer']}\n\nSources : {', '.join(demo['sources'])}\nLimites : {'; '.join(demo['limitations'])}"
        st.session_state["chat_history"].append({"role": "assistant", "text": assistant_reply})
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

with status_col:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.markdown("<h3>Statut</h3>", unsafe_allow_html=True)
    if backend_ok:
        st.success("API active")
    else:
        st.warning("API hors ligne")
    st.write("Mode : démonstration")
    st.write("Pays : Sénégal")
    st.write("Langue : Français")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

left, right = st.columns(2)

with left:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.subheader("Recherche documentaire")
    search_query = st.text_input("Trouver une fiche de santé", value="hydratation")
    if st.button("Rechercher", key="search_docs"):
        if backend_ok:
            try:
                data = call_backend(f"/api/v1/health-information/search?q={search_query}&country=SN&language=fr", method="GET")
                st.session_state["source_result"] = data
            except RuntimeError as exc:
                st.error(str(exc))
                st.session_state["source_result"] = None
        else:
            st.session_state["source_result"] = {
                "count": 1,
                "results": [{
                    "title": "Hydratation de base",
                    "source": "Ministère de la Santé du Sénégal",
                    "content": "Boire régulièrement de l'eau et ajuster l'apport selon la chaleur et l'activité physique.",
                    "status": "validated",
                }],
            }

    if "source_result" in st.session_state:
        payload = st.session_state["source_result"]
        for item in payload.get("results", []):
            st.markdown(f"<div class='panel' style='margin-top: 0.75rem; padding: 0.9rem;'><strong>{item.get('title', 'Fiche')}</strong><br>{item.get('content', '')}<br><small>Source : {item.get('source', 'Inconnue')} | Statut : {item.get('status', 'inconnu')}</small></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.subheader("Parcours d'urgence")
    st.write("Simulation fictive pour tester le triage et la logique de conduite.")
    if not st.session_state.get("emergency_session_id"):
        if st.button("Démarrer le parcours"):
            if backend_ok:
                try:
                    data = call_backend("/api/v1/emergency/session", method="POST", payload={"country": "SN", "language": "fr", "scenario": "demo"})
                    st.session_state["emergency_session_id"] = data["session_id"]
                    st.session_state["emergency_step"] = data["next_question"]
                    st.session_state["emergency_guidance"] = data.get("guidance")
                    st.rerun()
                except RuntimeError as exc:
                    st.error(str(exc))
            else:
                st.session_state["emergency_session_id"] = "demo-offline-session"
                st.session_state["emergency_step"] = "Y a-t-il une hémorragie visible ou un état de conscience altéré ?"
                st.session_state["emergency_guidance"] = "Mode hors ligne simulé."
                st.rerun()
    if st.session_state.get("emergency_session_id"):
        session_id = st.session_state["emergency_session_id"]
        st.markdown(f"<div class='chip'>Session {session_id}</div>", unsafe_allow_html=True)
        st.info(st.session_state.get("emergency_step", "Aucune étape en cours."))
        st.write(st.session_state.get("emergency_guidance", ""))
        choice = st.radio("Votre réponse", ["Oui", "Non"], index=None, key="emergency_choice")
        if st.button("Valider", key="validate_emergency") and choice is not None:
            answer = "oui" if choice == "Oui" else "non"
            if backend_ok:
                try:
                    data = call_backend(f"/api/v1/emergency/session/{session_id}/answer", method="POST", payload={"answer": answer})
                    st.session_state["emergency_step"] = data.get("next_question")
                    st.session_state["emergency_guidance"] = data.get("guidance")
                    st.success(str(data))
                except RuntimeError as exc:
                    st.error(str(exc))
            else:
                demo = get_demo_sources()["urgent"]
                st.info(demo["answer"])
                for item in demo["limitations"]:
                    st.write(f"- {item}")
                reset_emergency_session()
        if st.button("Réinitialiser", key="reset_emergency"):
            reset_emergency_session()
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

med_col, med_detail_col = st.columns([1.2, 1])

with med_col:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.subheader("Reconnaissance de médicament")
    uploaded = st.file_uploader("Téléverser une image de boîte ou de notice", type=["jpg", "jpeg", "png", "webp"])
    if uploaded is not None:
        if st.button("Analyser l'image", key="analyze_med"):
            payload = {
                "file_name": uploaded.name,
                "content_type": uploaded.type or "image/jpeg",
                "size_bytes": uploaded.size,
            }
            if backend_ok:
                try:
                    data = call_backend("/api/v1/medications/recognize", method="POST", payload=payload)
                    st.session_state["medication_result"] = data
                except RuntimeError as exc:
                    st.error(str(exc))
                    st.session_state["medication_result"] = None
            else:
                st.session_state["medication_result"] = {
                    "status": "ambiguous",
                    "requires_confirmation": True,
                    "message": "Simulation hors ligne : image reçue, reconnaissance non fiable sans OCR validé.",
                    "candidates": [
                        {"candidate_id": "demo-01", "display_name": "Médicament A (fiction)", "confidence": 0.62},
                        {"candidate_id": "demo-02", "display_name": "Médicament B (fiction)", "confidence": 0.41},
                    ],
                }
    if "medication_result" in st.session_state:
        st.json(st.session_state["medication_result"])
    st.markdown("</div>", unsafe_allow_html=True)

with med_detail_col:
    st.markdown("<div class='panel'>", unsafe_allow_html=True)
    st.subheader("Points de vigilance")
    st.write("- Une identification par image n'est jamais certaine.")
    st.write("- Aucune dose personnalisée n'est calculée.")
    st.write("- Les résultats sont démonstratifs et non médicaux.")
    st.write("- Vérifiez toujours auprès d'un professionnel si besoin.")
    st.markdown("</div>", unsafe_allow_html=True)
