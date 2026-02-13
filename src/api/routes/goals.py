"""
Goals API routes.
Handles nutrition goals storage.
"""

from fastapi import APIRouter
from pydantic import BaseModel

from src.api.schemas import GoalsCreate, GoalsResponse, SuccessResponse

router = APIRouter(prefix="/goals", tags=["goals"])


class GoalsStorage:
    """Simple file-based goals storage (can be replaced with database)."""
    
    def __init__(self):
        self._goals = {
            "protein": 0.0,
            "fat": 0.0,
            "carbohydrates": 0.0,
            "calories": 0.0
        }
    
    def get(self) -> dict:
        """Get current goals."""
        return self._goals.copy()
    
    def set(self, goals: GoalsCreate) -> dict:
        """Set new goals."""
        self._goals = {
            "protein": goals.protein,
            "fat": goals.fat,
            "carbohydrates": goals.carbohydrates,
            "calories": goals.calories,
        }
        return self._goals.copy()


# Global storage instance
_goals_storage = GoalsStorage()


class GoalsResponseWithStatus(BaseModel):
    """Response with status and goals."""
    status: str = "success"
    goals: GoalsResponse


@router.get("", response_model=GoalsResponse)
async def get_goals():
    """
    Get current nutrition goals.
    
    Returns the currently stored nutrition goals.
    """
    return GoalsResponse(**_goals_storage.get())


@router.post("", response_model=GoalsResponseWithStatus)
async def set_goals(goals: GoalsCreate):
    """
    Set nutrition goals.
    
    Updates the stored nutrition goals with new values.
    """
    updated_goals = _goals_storage.set(goals)
    return GoalsResponseWithStatus(
        status="success",
        goals=GoalsResponse(**updated_goals)
    )
