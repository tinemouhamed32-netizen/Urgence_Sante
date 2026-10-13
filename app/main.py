from __future__ import annotations

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.database.session import init_db
from app.schemas.common import RootResponse

init_db()

app = FastAPI(
    title="Urgence Santé",
    version="0.1.0",
    description=(
        "Prototype d'IA d'assistance sanitaire en mode démonstration. "
        "Les réponses sont conçues pour l'analyse, la démonstration et la validation technique, "
        "et ne remplacent pas un avis médical professionnel."
    ),
    summary="Plateforme de démonstration pour l'assistance sanitaire et le triage d'urgence.",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "health", "description": "Endpoints de contrôle de santé et de validation de paramètres."},
        {"name": "assistant", "description": "Assistant de santé général et réponse guidée par le moteur de démonstration."},
        {"name": "emergency", "description": "Parcours d'urgence et protocoles de démonstration."},
        {"name": "medications", "description": "Reconnaissance de médicament et validation de notice de démonstration."},
        {"name": "health_information", "description": "Recherche documentaire et sources de santé de démonstration."},
    ],
    contact={
        "name": "Urgence Santé Demo",
    },
    license_info={
        "name": "Prototype uniquement",
        "url": "https://example.com/license",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        origin.strip()
        for origin in os.getenv("CORS_ALLOWED_ORIGINS", "*").split(",")
        if origin.strip()
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/", response_model=RootResponse, summary="Page d'accueil de l'API")
def root() -> RootResponse:
    return RootResponse(message="Bienvenue dans Urgence Santé", version="0.1.0")
