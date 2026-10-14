from __future__ import annotations

import os
from html import escape
from typing import Any

import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")
if "://" not in BACKEND_URL:
    BACKEND_URL = f"https://{BACKEND_URL}"

st.set_page_config(
    page_title="Urgence Santé | Assistant IA",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    :root {
        --ink: #172d2a;
        --muted: #637772;
        --primary: #167765;
        --primary-dark: #105e51;
        --line: #e3ebe8;
        --surface: #ffffff;
        --canvas: #f5f8f7;
        --subtle: #edf4f1;
    }
    .stApp {
        background: var(--canvas);
        color: var(--ink);
    }
    .block-container {
        max-width: 1280px;
        padding: 1.4rem 2.5rem 4rem;
    }
    header[data-testid="stHeader"] {
        background: rgba(245, 248, 247, 0.9);
    }
    h1, h2, h3, h4, p, label, [data-testid="stMarkdownContainer"] {
        color: var(--ink);
    }
    h3, [data-testid="stSubheader"] {
        letter-spacing: -0.025em;
    }
    [data-testid="stCaptionContainer"] {
        color: var(--muted);
    }
    .app-topbar {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin: 0.1rem 0 1.5rem;
    }
    .brand-icon {
        display: grid;
        place-items: center;
        width: 2.5rem;
        height: 2.5rem;
        border: 1px solid rgba(255, 255, 255, 0.16);
        border-radius: 0.8rem;
        background: var(--primary-dark);
        color: white;
        font-size: 1.45rem;
        font-weight: 600;
        box-shadow: 0 5px 12px rgba(16, 94, 81, 0.13);
    }
    .brand-name {
        color: var(--ink);
        font-size: 1rem;
        font-weight: 750;
        line-height: 1.2;
    }
    .brand-caption {
        color: var(--muted);
        font-size: 0.78rem;
        margin-top: 0.1rem;
    }
    .topbar-tag {
        margin-left: auto;
        padding: 0.4rem 0.68rem;
        border: 1px solid var(--line);
        border-radius: 999px;
        color: #536b65;
        background: var(--surface);
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.035em;
    }
    .hero-card {
        position: relative;
        overflow: hidden;
        display: grid;
        grid-template-columns: minmax(0, 1.55fr) minmax(210px, 0.65fr);
        align-items: center;
        gap: 2rem;
        padding: clamp(1.6rem, 4vw, 2.8rem);
        border: 1px solid #1c5c50;
        border-radius: 1.2rem;
        background: linear-gradient(118deg, #123a35 0%, #155548 100%);
        box-shadow: 0 12px 30px rgba(24, 61, 53, 0.11);
        margin-bottom: 1.2rem;
    }
    .hero-eyebrow {
        color: #b7dece;
        font-size: 0.76rem;
        font-weight: 750;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 0.7rem;
    }
    .hero-card .hero-title {
        max-width: 660px;
        margin: 0;
        color: #f5faf8;
        font-size: clamp(2rem, 4vw, 3.15rem);
        font-weight: 720;
        letter-spacing: -0.05em;
        line-height: 1.08;
    }
    .hero-copy {
        max-width: 620px;
        margin: 0.9rem 0 0;
        color: #d2e7df;
        font-size: 0.98rem;
        line-height: 1.7;
    }
    .hero-note {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        margin-top: 1.1rem;
        padding: 0.48rem 0.7rem;
        border: 1px solid rgba(223, 255, 241, 0.18);
        border-radius: 0.65rem;
        background: rgba(8, 43, 37, 0.22);
        color: #e0efe9;
        font-size: 0.78rem;
        font-weight: 650;
    }
    .hero-aside {
        padding: 1.15rem 1.2rem;
        border: 1px solid rgba(230, 249, 241, 0.16);
        border-radius: 0.9rem;
        background: rgba(255, 255, 255, 0.07);
    }
    .hero-aside-label {
        color: #b7dece;
        font-size: 0.7rem;
        font-weight: 750;
        letter-spacing: 0.09em;
        text-transform: uppercase;
    }
    .hero-aside-title {
        margin-top: 0.55rem;
        color: #f4faf7;
        font-size: 1.05rem;
        font-weight: 700;
        line-height: 1.35;
    }
    .hero-aside-copy {
        margin-top: 0.5rem;
        color: #c8ddd5;
        font-size: 0.82rem;
        line-height: 1.55;
    }
    .section-heading {
        margin: 1.8rem 0 0.85rem;
        color: var(--ink);
        font-size: 1.16rem;
        font-weight: 750;
    }
    .panel {
        margin-top: 0.8rem;
        padding: 1rem 1.05rem;
        border: 1px solid var(--line);
        border-radius: 0.8rem;
        background: #f8fbf9;
        line-height: 1.6;
    }
    .panel small {
        display: inline-block;
        margin-top: 0.55rem;
        color: var(--muted);
    }
    .panel-anchor {
        display: none;
    }
    .stHorizontalBlock > div[data-testid="column"]:has(.panel-anchor) > div[data-testid="stVerticalBlock"] {
        height: 100%;
        padding: 1.2rem 1.25rem;
        border: 1px solid var(--line);
        border-radius: 0.95rem;
        background: var(--surface);
        box-shadow: 0 3px 12px rgba(31, 70, 61, 0.035);
    }
    .stHorizontalBlock {
        gap: 1.1rem;
    }
    .metric-card {
        min-height: 88px;
        padding: 0.95rem 1rem;
        border: 1px solid var(--line);
        border-radius: 0.8rem;
        background: var(--surface);
        box-shadow: 0 2px 8px rgba(31, 70, 61, 0.025);
    }
    .metric-value {
        color: var(--primary-dark);
        font-size: 1.28rem;
        font-weight: 750;
        line-height: 1.15;
    }
    .metric-label {
        margin-top: 0.38rem;
        color: var(--muted);
        font-size: 0.78rem;
        font-weight: 600;
    }
    .badge {
        display: inline-block;
        padding: 0.36rem 0.65rem;
        border: 1px solid #dcebe5;
        border-radius: 0.55rem;
        background: var(--subtle);
        color: var(--primary-dark);
        font-size: 0.72rem;
        font-weight: 750;
        letter-spacing: 0.045em;
        text-transform: uppercase;
    }
    .chip {
        display: inline-flex;
        align-items: center;
        padding: 0.34rem 0.65rem;
        border: 1px solid #eedcb7;
        border-radius: 0.55rem;
        background: #fff8e9;
        color: #805c17;
        font-size: 0.78rem;
        font-weight: 700;
    }
    .reply-user, .reply-assistant {
        margin-bottom: 0.7rem;
        padding: 0.85rem 0.95rem;
        border-radius: 0.75rem;
        color: var(--ink);
        line-height: 1.6;
        overflow-wrap: anywhere;
    }
    .reply-user {
        border: 1px solid #dce7ef;
        background: #f4f8fb;
    }
    .reply-assistant {
        border: 1px solid #dce9e3;
        background: #f4f8f5;
    }
    .stButton > button, .stFormSubmitButton > button {
        min-height: 2.65rem;
        border: 1px solid var(--primary);
        border-radius: 0.65rem;
        background: var(--primary);
        color: #fff;
        font-weight: 700;
        transition: background 120ms ease, border-color 120ms ease;
    }
    .stButton > button:hover, .stFormSubmitButton > button:hover {
        border-color: var(--primary-dark);
        background: var(--primary-dark);
        color: #fff;
    }
    .stButton > button:focus-visible, .stFormSubmitButton > button:focus-visible {
        outline: 3px solid rgba(22, 119, 101, 0.25);
        outline-offset: 2px;
    }
    input, textarea, [data-baseweb="select"] > div {
        border-radius: 0.6rem !important;
    }
    .stTextInput input, .stTextArea textarea {
        border-color: var(--line) !important;
        background: #fff !important;
        color: var(--ink) !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.35rem;
        border-bottom: 1px solid var(--line);
    }
    .stTabs [data-baseweb="tab"] {
        padding: 0.75rem 1rem;
        color: var(--muted);
        font-weight: 650;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: var(--primary-dark);
        border-bottom-color: var(--primary);
    }
    div[data-testid="stAlert"] {
        border-radius: 0.7rem;
    }
    [data-testid="stSidebar"] {
        border-right: 1px solid var(--line);
        background: #fbfcfb;
    }
    [data-testid="stSidebar"] .block-container {
        padding: 1.4rem 1.15rem 2rem;
    }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] li {
        color: #536963;
        font-size: 0.9rem;
        line-height: 1.65;
    }
    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after {
            scroll-behavior: auto !important;
            transition-duration: 0.01ms !important;
        }
    }
    @media (max-width: 760px) {
        .block-container {
            padding: 1rem 1rem 2.5rem;
        }
        .hero-card {
            grid-template-columns: 1fr;
            gap: 1.15rem;
            padding: 1.45rem 1.25rem;
            border-radius: 0.95rem;
        }
        .hero-card .hero-title {
            font-size: clamp(1.9rem, 8vw, 2.6rem);
        }
        .hero-aside {
            padding: 0.95rem 1rem;
        }
        .topbar-tag {
            font-size: 0.62rem;
            padding: 0.36rem 0.55rem;
        }
        .hero-copy {
            font-size: 0.94rem;
        }
        .stHorizontalBlock {
            gap: 0.75rem;
        }
        .stHorizontalBlock > div[data-testid="column"]:has(.panel-anchor) > div[data-testid="stVerticalBlock"] {
            padding: 1rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("<div class='badge'>Assistant santé IA</div>", unsafe_allow_html=True)
    st.subheader("Comment utiliser l’outil")
    st.caption("Choisissez un parcours selon votre besoin.")
    st.markdown("---")
    st.markdown(
        """
        **01 · Poser une question**

        Conseils généraux et prévention.

        **02 · Vérifier une source**

        Fiches documentaires du corpus de démonstration.

        **03 · Tester un parcours**

        Simulation de triage ou de reconnaissance.
        """
    )
    st.markdown("---")
    st.caption("Prototype de hackathon · Sénégal")
    st.caption("N’entrez aucune donnée permettant d’identifier une personne.")

st.markdown(
    """
    <div class="app-topbar">
      <div class="brand-icon">+</div>
      <div>
        <div class="brand-name">Urgence Santé</div>
        <div class="brand-caption">Votre espace d’information santé</div>
      </div>
      <div class="topbar-tag">Démonstration · Sénégal</div>
    </div>
    <section class="hero-card">
      <div>
        <div class="hero-eyebrow">Un repère pour vos questions de santé</div>
        <h1 class="hero-title">Mieux comprendre, mieux s’orienter.</h1>
        <p class="hero-copy">Explorez des informations générales, consultez leurs sources et découvrez des simulations d’urgence fictives.</p>
        <div class="hero-note">Information indicative · Ne remplace pas un professionnel de santé</div>
      </div>
      <aside class="hero-aside">
        <div class="hero-aside-label">Notre engagement</div>
        <div class="hero-aside-title">Des réponses utiles, avec leurs limites.</div>
        <div class="hero-aside-copy">Aucun diagnostic ni traitement personnalisé. En cas d’urgence réelle, contactez immédiatement les services de secours.</div>
      </aside>
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown("### Un point de départ, selon votre besoin")
st.caption("Des outils simples, des sources visibles et des limites clairement indiquées.")

metric_cols = st.columns(3)
with metric_cols[0]:
    st.markdown("<div class='metric-card'><div class='metric-value'>Assistant santé</div><div class='metric-label'>Questions générales et prévention</div></div>", unsafe_allow_html=True)
with metric_cols[1]:
    st.markdown("<div class='metric-card'><div class='metric-value'>Sources consultables</div><div class='metric-label'>Fiches d’information documentées</div></div>", unsafe_allow_html=True)
with metric_cols[2]:
    st.markdown("<div class='metric-card'><div class='metric-value'>Mode démonstration</div><div class='metric-label'>Scénarios fictifs · sans diagnostic</div></div>", unsafe_allow_html=True)

def call_backend(
    path: str,
    *,
    method: str = "GET",
    payload: dict | None = None,
    params: dict[str, str] | None = None,
) -> Any:
    url = f"{BACKEND_URL}{path}"
    try:
        with st.spinner("Connexion au service…"):
            if method == "GET":
                response = requests.get(url, params=params, timeout=60)
            else:
                response = requests.post(url, json=payload, timeout=60)
    except requests.RequestException as exc:
        raise RuntimeError("Le service est momentanément indisponible. Réessayez dans quelques instants.") from exc

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        data = {}
    if not response.ok:
        detail = data.get("detail") if isinstance(data, dict) else None
        raise BackendResponseError(
            str(detail or f"Le service a répondu avec le code {response.status_code}."),
            status_code=response.status_code,
        )
    return data


class BackendResponseError(RuntimeError):
    def __init__(self, message: str, *, status_code: int) -> None:
        super().__init__(message)
        self.status_code = status_code


def reset_emergency_session() -> None:
    st.session_state.pop("emergency_session_id", None)
    st.session_state.pop("emergency_step", None)
    st.session_state.pop("emergency_guidance", None)
    st.session_state.pop("emergency_status", None)
    st.session_state.pop("emergency_choice", None)
    st.session_state.pop("emergency_error", None)


if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = [
        {"role": "assistant", "text": "Bonjour ! Je peux vous aider à explorer des informations générales de prévention. Choisissez un sujet et je vous indiquerai les sources et les limites de la réponse."}
    ]

assistant_tab, sources_tab, emergency_tab, medication_tab = st.tabs(
    ["Assistant", "Fiches santé", "Parcours d’urgence", "Médicament · simulation"]
)

with assistant_tab:
    st.markdown("<div class='panel-anchor'></div>", unsafe_allow_html=True)
    st.markdown("<h3>Posez votre question</h3>", unsafe_allow_html=True)
    st.caption("Réponses issues du corpus de démonstration, avec leurs sources et leurs limites.")

    for message in st.session_state["chat_history"]:
        role = message["role"]
        bubble_class = "reply-user" if role == "user" else "reply-assistant"
        label = "Vous" if role == "user" else "Assistant"
        text = escape(message["text"]).replace("\n", "<br>")
        st.markdown(f"<div class='{bubble_class}'><strong>{label}</strong><br>{text}</div>", unsafe_allow_html=True)

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Votre message", placeholder="Posez une question de santé générale ...")
        submitted = st.form_submit_button("Envoyer")

    if submitted and user_input.strip():
        st.session_state["chat_history"].append({"role": "user", "text": user_input.strip()})
        try:
            data = call_backend(
                "/api/v1/assistant/message",
                method="POST",
                payload={"question": user_input.strip(), "country": "SN", "language": "fr"},
            )
            reply = data.get("answer", "Aucune réponse disponible.")
            sources = ", ".join(data.get("sources", [])) or "Aucune source listée."
            limitations = "; ".join(data.get("limitations", [])) or "Aucune limite précisée."
            assistant_reply = f"{reply}\n\nSources : {sources}\nLimites : {limitations}"
            if data.get("category") == "emergency":
                assistant_reply += "\n\nPour une situation réelle, contactez immédiatement les services de secours locaux. Le parcours d’urgence de cette application est fictif."
        except RuntimeError as exc:
            assistant_reply = f"Je ne peux pas joindre le service pour le moment. {exc}"
        st.session_state["chat_history"].append({"role": "assistant", "text": assistant_reply})
        st.rerun()

with sources_tab:
    st.markdown("<div class='panel-anchor'></div>", unsafe_allow_html=True)
    st.markdown("<h3>Explorer les fiches documentaires</h3>", unsafe_allow_html=True)
    st.caption("Recherchez dans le corpus de démonstration consacré à la prévention et au bien-être.")
    with st.form("search_docs_form"):
        search_query = st.text_input("Sujet à rechercher", placeholder="Ex. hydratation, sommeil")
        search_submitted = st.form_submit_button("Rechercher dans les fiches")
    if search_submitted:
        if not search_query.strip():
            st.warning("Saisissez un sujet pour lancer la recherche.")
        else:
            try:
                st.session_state["source_result"] = call_backend(
                    "/api/v1/health-information/search",
                    params={"q": search_query.strip(), "country": "SN", "language": "fr"},
                )
                st.session_state.pop("source_error", None)
            except BackendResponseError as exc:
                st.session_state.pop("source_result", None)
                if exc.status_code == 404:
                    st.session_state.pop("source_error", None)
                    st.session_state["source_result"] = {"count": 0, "results": []}
                else:
                    st.session_state["source_error"] = str(exc)
            except RuntimeError as exc:
                st.session_state.pop("source_result", None)
                st.session_state["source_error"] = str(exc)

    if st.session_state.get("source_error"):
        st.error(st.session_state["source_error"])
    if "source_result" in st.session_state:
        payload = st.session_state["source_result"]
        results = payload.get("results", [])
        if not results:
            st.info("Aucune fiche ne correspond à cette recherche dans le corpus de démonstration.")
        else:
            st.caption(f"{len(results)} fiche(s) trouvée(s)")
        for item in results:
            title = escape(str(item.get("title", "Fiche")))
            category = escape(str(item.get("category", "Information générale")))
            content = escape(str(item.get("content", "")))
            source = escape(str(item.get("source", "Source non précisée")))
            last_verified = escape(str(item.get("last_verified") or "Date non précisée"))
            st.markdown(
                f"<div class='panel'><span class='badge'>{category}</span><h4>{title}</h4>{content}<br>"
                f"<small>Source : {source} · Vérifiée le : {last_verified} · Contenu de démonstration</small></div>",
                unsafe_allow_html=True,
            )

with emergency_tab:
    st.markdown("<div class='panel-anchor'></div>", unsafe_allow_html=True)
    st.markdown("<h3>Parcours d’urgence · simulation guidée</h3>", unsafe_allow_html=True)
    st.warning("Parcours entièrement fictif : il ne constitue pas un triage médical. Pour toute urgence réelle, contactez immédiatement les secours locaux.")
    st.write("Répondez aux étapes du scénario pour découvrir le fonctionnement du parcours de démonstration.")
    if not st.session_state.get("emergency_session_id"):
        if st.button("Commencer la simulation", key="start_emergency"):
            try:
                data = call_backend(
                    "/api/v1/emergency/session",
                    method="POST",
                    payload={"country": "SN", "language": "fr"},
                )
                st.session_state["emergency_session_id"] = data["session_id"]
                st.session_state["emergency_step"] = data.get("next_question")
                st.session_state["emergency_guidance"] = data.get("guidance")
                st.session_state["emergency_status"] = data.get("status")
                st.rerun()
            except RuntimeError as exc:
                st.error(str(exc))
    if st.session_state.get("emergency_session_id"):
        session_id = st.session_state["emergency_session_id"]
        st.markdown(f"<div class='chip'>Session {escape(session_id)}</div>", unsafe_allow_html=True)
        next_question = st.session_state.get("emergency_step")
        if next_question:
            st.info(next_question)
            if st.session_state.get("emergency_guidance"):
                st.caption(st.session_state["emergency_guidance"])
            choice = st.radio("Votre réponse", ["Oui", "Non"], index=None, key="emergency_choice")
            if st.button("Valider ma réponse", key="validate_emergency"):
                if choice is None:
                    st.warning("Choisissez « Oui » ou « Non » pour continuer.")
                else:
                    answer = "oui" if choice == "Oui" else "non"
                    try:
                        data = call_backend(
                            f"/api/v1/emergency/session/{session_id}/answer",
                            method="POST",
                            payload={"answer": answer},
                        )
                        st.session_state["emergency_step"] = data.get("next_question")
                        st.session_state["emergency_guidance"] = data.get("guidance")
                        st.session_state["emergency_status"] = data.get("status")
                        st.session_state.pop("emergency_choice", None)
                        st.rerun()
                    except RuntimeError as exc:
                        st.error(str(exc))
        else:
            if st.session_state.get("emergency_status") == "requires_immediate_help":
                st.error("Fin de la simulation : ce scénario fictif signale un besoin d’aide immédiate.")
                st.write("Dans une situation réelle, contactez les secours locaux. Ne vous fiez pas à ce résultat simulé.")
            else:
                st.success("Fin de la simulation.")
            if st.session_state.get("emergency_guidance"):
                st.caption(st.session_state["emergency_guidance"])
        if st.button("Réinitialiser la simulation", key="reset_emergency"):
            reset_emergency_session()
            st.rerun()

with medication_tab:
    st.markdown("<div class='panel-anchor'></div>", unsafe_allow_html=True)
    st.markdown("<h3>Tester le parcours de lecture d’une boîte</h3>", unsafe_allow_html=True)
    st.warning("La reconnaissance OCR n’est pas encore intégrée : les candidats ci-dessous sont fictifs et ne permettent pas d’identifier un médicament.")
    with st.expander("Comment fonctionne cette démonstration ?", expanded=True):
        st.write("L’image est utilisée uniquement pour illustrer le parcours dans cette interface. Seuls son nom, son type et sa taille sont envoyés au moteur de démonstration ; l’image n’est ni transmise à une IA externe ni enregistrée.")
    uploaded = st.file_uploader(
        "Choisir une image de boîte ou de notice",
        type=["jpg", "jpeg", "png", "webp"],
        help="Image de démonstration uniquement · 5 Mo maximum.",
    )
    if uploaded is not None:
        st.image(uploaded, caption="Aperçu local de l’image", width=320)
        if st.button("Lancer la simulation de lecture", key="analyze_med"):
            payload = {
                "file_name": uploaded.name,
                "content_type": uploaded.type or "image/jpeg",
                "size_bytes": uploaded.size,
            }
            try:
                st.session_state["medication_result"] = call_backend(
                    "/api/v1/medications/recognize",
                    method="POST",
                    payload=payload,
                )
                st.session_state.pop("medication_confirmation", None)
            except RuntimeError as exc:
                st.error(str(exc))
    if "medication_result" in st.session_state:
        result = st.session_state["medication_result"]
        st.info(result.get("message", "Résultat de la simulation."))
        candidates = result.get("candidates", [])
        for candidate in candidates:
            name = escape(str(candidate.get("display_name", "Candidat fictif")))
            notes = escape(str(candidate.get("notes", "Aucune information supplémentaire.")))
            st.markdown(
                f"<div class='panel'><strong>{name}</strong><br>{notes}<br>"
                "<small>Résultat fictif · Non utilisable pour une décision de santé</small></div>",
                unsafe_allow_html=True,
            )
        if candidates:
            candidate_labels = {
                candidate["candidate_id"]: candidate["display_name"]
                for candidate in candidates
            }
            selected_candidate = st.selectbox(
                "Candidat à tester",
                options=list(candidate_labels),
                format_func=lambda candidate_id: candidate_labels[candidate_id],
                key="medication_candidate",
            )
            if st.button("Tester la confirmation (simulation)", key="confirm_med"):
                try:
                    st.session_state["medication_confirmation"] = call_backend(
                        "/api/v1/medications/confirm",
                        method="POST",
                        payload={
                            "candidate_id": selected_candidate,
                            "confirmed": True,
                            "question": "Confirmation de démonstration",
                        },
                    )
                except RuntimeError as exc:
                    st.error(str(exc))
        if st.session_state.get("medication_confirmation"):
            confirmation = st.session_state["medication_confirmation"]
            st.success(confirmation.get("message", "Confirmation de démonstration enregistrée."))
            for warning in confirmation.get("warnings", []):
                st.warning(warning)

    st.markdown("---")
    st.markdown("**Pour un vrai médicament**")
    st.write("Vérifiez la boîte et la notice auprès d’un pharmacien ou d’un professionnel de santé. N’utilisez jamais une reconnaissance automatisée pour choisir une dose ou un traitement.")
