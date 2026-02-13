"""
Dish API routes.
Uses repository pattern for data access.
"""

from fastapi import APIRouter, Depends, Query
from typing import List

from sqlalchemy.orm import Session

from src.api.schemas import (
    DishResponse,
    DishDetailResponse,
    DishCreate,
    DishUpdate,
    SuccessResponse,
    NotFoundError,
    BadRequestError,
    ConflictError,
)
from src.database import get_db
from src.repositories import DishRepository, IngredientRepository
from src.services.nutrition_service import NutritionService

router = APIRouter(prefix="/dishes", tags=["dishes"])


def get_dish_repository(db: Session = Depends(get_db)) -> DishRepository:
    """Dependency to get DishRepository instance."""
    return DishRepository(db)


def get_ingredient_repository(db: Session = Depends(get_db)) -> IngredientRepository:
    """Dependency to get IngredientRepository instance."""
    return IngredientRepository(db)


@router.get("", response_model=List[DishResponse])
async def get_dishes(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records"),
    repo: DishRepository = Depends(get_dish_repository),
    ing_repo: IngredientRepository = Depends(get_ingredient_repository),
):
    """
    Get all dishes with calculated nutrition.
    
    Supports pagination with skip and limit parameters.
    """
    nutrition_service = NutritionService(repo, ing_repo)
    return nutrition_service.get_dishes_with_nutrition(skip=skip, limit=limit)


@router.get("/{dish_id}", response_model=DishDetailResponse)
async def get_dish(
    dish_id: int,
    repo: DishRepository = Depends(get_dish_repository),
    ing_repo: IngredientRepository = Depends(get_ingredient_repository),
):
    """
    Get dish details with ingredients.
    
    Raises:
        NotFoundError: If dish not found
    """
    nutrition_service = NutritionService(repo, ing_repo)
    result = nutrition_service.get_dish_with_ingredients(dish_id)
    
    if not result:
        raise NotFoundError("Dish", str(dish_id))
    
    return result


@router.post("/new", response_model=SuccessResponse)
async def create_dish(
    dish: DishCreate,
    repo: DishRepository = Depends(get_dish_repository),
    ing_repo: IngredientRepository = Depends(get_ingredient_repository),
):
    """
    Create a new dish.
    
    Raises:
        ConflictError: If dish name already exists
        BadRequestError: If ingredients list is empty or invalid
    """
    # Check if dish name already exists
    if repo.name_exists(dish.name):
        raise ConflictError(f"Dish '{dish.name}' already exists")
    
    # Validate ingredients
    if not dish.ingredients:
        raise BadRequestError("Dish must have at least one ingredient")
    
    # Convert ingredients to dict format
    ingredients_dict = {ing.name: ing.amount for ing in dish.ingredients}
    
    # Validate all ingredients exist
    for ing_name in ingredients_dict.keys():
        if not ing_repo.get_by_name(ing_name):
            raise BadRequestError(f"Ingredient '{ing_name}' not found")
    
    try:
        repo.create_dish(dish.name, ingredients_dict)
        return SuccessResponse(message=f"Dish '{dish.name}' created successfully")
    except ValueError as e:
        raise BadRequestError(str(e))


@router.post("/{dish_id}", response_model=SuccessResponse)
async def update_dish(
    dish_id: int,
    dish_update: DishUpdate,
    repo: DishRepository = Depends(get_dish_repository),
    ing_repo: IngredientRepository = Depends(get_ingredient_repository),
):
    """
    Update dish ingredients.
    
    Raises:
        NotFoundError: If dish not found
        BadRequestError: If ingredients list is empty or invalid
    """
    # Check dish exists
    if not repo.exists(dish_id):
        raise NotFoundError("Dish", str(dish_id))
    
    # Validate ingredients
    if not dish_update.ingredients:
        raise BadRequestError("Dish must have at least one ingredient")
    
    # Convert ingredients to dict format
    ingredients_dict = {ing.name: ing.amount for ing in dish_update.ingredients}
    
    # Validate all ingredients exist
    for ing_name in ingredients_dict.keys():
        if not ing_repo.get_by_name(ing_name):
            raise BadRequestError(f"Ingredient '{ing_name}' not found")
    
    try:
        repo.update_dish_ingredients(dish_id, ingredients_dict)
        return SuccessResponse(message="Dish updated successfully")
    except ValueError as e:
        raise BadRequestError(str(e))


@router.delete("/{dish_id}", response_model=SuccessResponse)
async def delete_dish(
    dish_id: int,
    repo: DishRepository = Depends(get_dish_repository),
):
    """
    Delete a dish.
    
    Raises:
        NotFoundError: If dish not found
    """
    if not repo.delete_dish(dish_id):
        raise NotFoundError("Dish", str(dish_id))
    
    return SuccessResponse(message="Dish deleted successfully")
