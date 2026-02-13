from fastapi import APIRouter
from src.api.schemas import GoalsCreate, GoalsResponse, SuccessResponse

router = APIRouter(prefix="/goals", tags=["goals"])

# In-memory storage for goals (will be replaced with database later)
_goals_storage = {
    "protein": 0,
    "fat": 0,
    "carbohydrates": 0,
    "calories": 0
}


@router.get("", response_model=GoalsResponse)
async def get_goals():
    """Get current nutrition goals."""
    return GoalsResponse(**_goals_storage)


@router.post("", response_model=SuccessResponse)
async def set_goals(goals: GoalsCreate):
    """Set nutrition goals."""
    global _goals_storage
    _goals_storage = {
        "protein": goals.protein,
        "fat": goals.fat,
        "carbohydrates": goals.carbohydrates,
        "calories": goals.calories,
    }
    return SuccessResponse()
