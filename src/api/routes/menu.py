from fastapi import APIRouter, Depends
from src.api.schemas import (
    MenuProcessRequest,
    MenuProcessResponse,
    IngredientSummary,
)
from src.services.dish_service import DishService
from src.models.dish_loader import DishLoader
from src.models.ingredient_data_loader import IngredientDataLoader
from src.models.nutrition_calculator import NutritionCalculator

router = APIRouter(tags=["menu"])


def get_dish_service() -> DishService:
    """Dependency to get DishService instance."""
    dish_loader = DishLoader()
    ingredient_loader = IngredientDataLoader()
    nutrition_calculator = NutritionCalculator()
    return DishService(dish_loader, ingredient_loader, nutrition_calculator)


@router.post("/menu", response_model=MenuProcessResponse)
async def process_menu(
    request: MenuProcessRequest,
    service: DishService = Depends(get_dish_service)
):
    """Process menu and calculate ingredient amounts."""
    selected_dishes = [{"id": d.id, "portions": d.portions} for d in request.dishes]
    result = service.process_menu(selected_dishes)
    
    # Convert to response format
    ingredients = {
        name: IngredientSummary(amount=data["amount"], unit=data["unit"])
        for name, data in result["ingredients"].items()
    }
    
    return MenuProcessResponse(ingredients=ingredients)
