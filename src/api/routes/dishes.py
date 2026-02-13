from fastapi import APIRouter, HTTPException, Depends
from typing import List

from src.api.schemas import (
    DishResponse,
    DishDetailResponse,
    DishCreate,
    DishUpdate,
    DishIngredientUpdate,
    MenuProcessRequest,
    MenuProcessResponse,
    IngredientSummary,
    SuccessResponse,
)
from src.services.dish_service import DishService
from src.models.dish_loader import DishLoader
from src.models.ingredient_data_loader import IngredientDataLoader
from src.models.nutrition_calculator import NutritionCalculator

router = APIRouter(prefix="/dishes", tags=["dishes"])


def get_dish_service() -> DishService:
    """Dependency to get DishService instance."""
    dish_loader = DishLoader()
    ingredient_loader = IngredientDataLoader()
    nutrition_calculator = NutritionCalculator()
    return DishService(dish_loader, ingredient_loader, nutrition_calculator)


@router.get("", response_model=List[DishResponse])
async def get_dishes(service: DishService = Depends(get_dish_service)):
    """Get all dishes with calculated nutrition."""
    return service.get_dishes()


@router.get("/{dish_id}", response_model=DishDetailResponse)
async def get_dish(dish_id: int, service: DishService = Depends(get_dish_service)):
    """Get dish details with ingredients."""
    try:
        return service.get_dish_ingredients(dish_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/new", response_model=SuccessResponse)
async def create_dish(
    dish: DishCreate,
    service: DishService = Depends(get_dish_service)
):
    """Create a new dish."""
    try:
        ingredients = [{"name": ing.name, "amount": ing.amount} for ing in dish.ingredients]
        service.create_dish(dish.name, ingredients)
        return SuccessResponse()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{dish_id}", response_model=SuccessResponse)
async def update_dish(
    dish_id: int,
    dish_update: DishUpdate,
    service: DishService = Depends(get_dish_service)
):
    """Update dish ingredients."""
    try:
        ingredients = [{"name": ing.name, "amount": ing.amount} for ing in dish_update.ingredients]
        service.update_dish(dish_id, ingredients)
        return SuccessResponse()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{dish_id}", response_model=SuccessResponse)
async def delete_dish(dish_id: int, service: DishService = Depends(get_dish_service)):
    """Delete a dish."""
    try:
        service.delete_dish(dish_id)
        return SuccessResponse()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


