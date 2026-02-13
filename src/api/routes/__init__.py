from fastapi import APIRouter
from .dishes import router as dishes_router
from .ingredients import router as ingredients_router
from .goals import router as goals_router
from .menu import router as menu_router

# Main API router that includes all sub-routers
api_router = APIRouter()

api_router.include_router(dishes_router)
api_router.include_router(ingredients_router)
api_router.include_router(goals_router)
api_router.include_router(menu_router)

__all__ = ["api_router"]
