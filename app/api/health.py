# app/api/health.py
# API endpoints for health check

from fastapi import APIRouter
from ..services.model_loader import get_models_status

# Create router
router = APIRouter(
    tags=["health"],
    responses={404: {"description": "Not found"}},
)

@router.get("/health")
async def health_check():
    """
    Basic health check endpoint
    """
    return {
        "status": "ok", 
        "models": get_models_status()
    }
