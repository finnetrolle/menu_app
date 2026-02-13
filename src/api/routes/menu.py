"""
Menu API routes.
Handles menu planning and ingredient aggregation.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict

from src.api.schemas import (
    MenuProcessRequest,
    MenuProcessResponse,
    IngredientSummary,
    SelectedDishSummary,
    NutritionSummary,
    BadRequestError,
)
from src.database import get_db
from src.repositories import DishRepository, IngredientRepository
from src.services.nutrition_service import NutritionService

router = APIRouter(tags=["menu"])


def get_dish_repository(db: Session = Depends(get_db)) -> DishRepository:
    """Dependency to get DishRepository instance."""
    return DishRepository(db)


def get_ingredient_repository(db: Session = Depends(get_db)) -> IngredientRepository:
    """Dependency to get IngredientRepository instance."""
    return IngredientRepository(db)


@router.post("/menu", response_model=MenuProcessResponse)
async def process_menu(
    request: MenuProcessRequest,
    dish_repo: DishRepository = Depends(get_dish_repository),
    ing_repo: IngredientRepository = Depends(get_ingredient_repository),
):
    """
    Process menu and calculate ingredient amounts.
    
    Takes a list of selected dishes with portions and returns:
    - List of dishes with portions
    - Aggregated shopping list with ingredient amounts
    - Total nutrition summary
    """
    if not request.dishes:
        return MenuProcessResponse(
            dishes=[],
            ingredients={},
            total_nutrition=NutritionSummary(
                protein=0,
                fat=0,
                carbohydrates=0,
                calories=0
            )
        )
    
    nutrition_service = NutritionService(dish_repo, ing_repo)
    
    # Get dish details and aggregate ingredients
    dishes_summary = []
    ingredients_aggregated: Dict[str, float] = {}
    
    for selected in request.dishes:
        dish = dish_repo.get_by_id_with_ingredients(selected.id)
        if not dish:
            continue
        
        # Add to dishes summary
        dishes_summary.append(SelectedDishSummary(
            id=selected.id,
            name=dish.name,
            portions=selected.portions
        ))
        
        # Aggregate ingredients
        for di in dish.ingredients:
            if di.ingredient:
                ingredient_name = di.ingredient.name
                total_amount = di.amount * selected.portions
                
                if ingredient_name in ingredients_aggregated:
                    ingredients_aggregated[ingredient_name] += total_amount
                else:
                    ingredients_aggregated[ingredient_name] = total_amount
    
    # Calculate total nutrition
    total_nutrition = nutrition_service.calculate_menu_nutrition(
        [{"id": d.id, "portions": d.portions} for d in request.dishes]
    )
    
    # Convert ingredients to response format
    ingredients = {
        name: IngredientSummary(amount=round(amount, 2), unit="г")
        for name, amount in sorted(ingredients_aggregated.items())
    }
    
    return MenuProcessResponse(
        dishes=dishes_summary,
        ingredients=ingredients,
        total_nutrition=NutritionSummary(
            protein=total_nutrition["protein"],
            fat=total_nutrition["fat"],
            carbohydrates=total_nutrition["carbohydrates"],
            calories=total_nutrition["calories"]
        )
    )
