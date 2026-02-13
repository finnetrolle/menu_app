from fastapi import APIRouter, Depends
from src.api.schemas import (
    MenuProcessRequest,
    MenuProcessResponse,
    IngredientSummary,
    SelectedDishSummary,
    NutritionSummary,
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
    
    # Get dish details for response
    dish_loader = DishLoader()
    dishes_summary = []
    total_protein =0.0
    total_fat = 0.0
    total_carbohydrates = 0.0
    total_calories = 0.0
    
    for selected in request.dishes:
        dish = dish_loader.get_dish_by_id(selected.id)
        if dish:
            dishes_summary.append(SelectedDishSummary(
                id=selected.id,
                name=dish.name,
                portions=selected.portions
            ))
            # Calculate nutrition for this dish
            total_protein += dish.protein_g * selected.portions
            total_fat += dish.fat_g * selected.portions
            total_carbohydrates += dish.carbohydrates_g * selected.portions
            total_calories += dish.energy_kcal * selected.portions
    
    # Convert ingredients to response format
    ingredients = {
        name: IngredientSummary(amount=data["amount"], unit=data["unit"])
        for name, data in result["ingredients"].items()
    }
    
    return MenuProcessResponse(
        dishes=dishes_summary,
        ingredients=ingredients,
        total_nutrition=NutritionSummary(
            protein=total_protein,
            fat=total_fat,
            carbohydrates=total_carbohydrates,
            calories=total_calories
        )
    )
