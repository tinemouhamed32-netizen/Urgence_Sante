from fastapi import APIRouter

from app.api.routes.assistant import router as assistant_router
from app.api.routes.emergency import router as emergency_router
from app.api.routes.health import router as health_router
from app.api.routes.health_information import router as health_information_router
from app.api.routes.medications import router as medications_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(emergency_router)
api_router.include_router(medications_router)
api_router.include_router(health_information_router)
api_router.include_router(assistant_router)
