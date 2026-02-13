"""
Ingredient API routes.
Uses repository pattern for data access.
"""

from fastapi import APIRouter, Depends, Query
from typing import List

from sqlalchemy.orm import Session

from src.api.schemas import (
    IngredientResponse,
    IngredientCreate,
    NutritionCreate,
    SuccessResponse,
    NotFoundError,
    ConflictError,
    BadRequestError,
)
from src.database import get_db
from src.repositories import IngredientRepository

router = APIRouter(prefix="/ingredients", tags=["ingredients"])


def get_ingredient_repository(db: Session = Depends(get_db)) -> IngredientRepository:
    """Dependency to get IngredientRepository instance."""
    return IngredientRepository(db)


@router.get("", response_model=List[IngredientResponse])
async def get_ingredients(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records"),
    search: str = Query(None, description="Search query for ingredient name"),
    repo: IngredientRepository = Depends(get_ingredient_repository),
):
    """
    Get all ingredients with optional search and pagination.
    
    Args:
        skip: Number of records to skip for pagination
        limit: Maximum number of records to return
        search: Optional search query to filter by name
        repo: Ingredient repository
        
    Returns:
        List of ingredients sorted by name
    """
    if search:
        ingredients = repo.search(search, limit=limit)
    else:
        ingredients = repo.get_all_sorted(skip=skip, limit=limit)
    
    return [
        IngredientResponse(
            id=ing.id,
            name=ing.name,
            nutrition=NutritionCreate(
                calories=_calculate_calories(ing.protein_g, ing.fat_g, ing.carbohydrates_g),
                proteins=ing.protein_g,
                fats=ing.fat_g,
                carbohydrates=ing.carbohydrates_g,
            )
        )
        for ing in ingredients
    ]


@router.post("", response_model=SuccessResponse)
async def create_ingredient(
    ingredient: IngredientCreate,
    repo: IngredientRepository = Depends(get_ingredient_repository),
):
    """
    Create a new ingredient.
    
    Raises:
        ConflictError: If ingredient name already exists
    """
    # Check if name already exists
    if repo.name_exists(ingredient.name):
        raise ConflictError(f"Ingredient '{ingredient.name}' already exists")
    
    # Create ingredient
    repo.create_ingredient(
        name=ingredient.name,
        protein_g=ingredient.nutrition.proteins,
        fat_g=ingredient.nutrition.fats,
        carbohydrates_g=ingredient.nutrition.carbohydrates,
    )
    
    return SuccessResponse(message=f"Ingredient '{ingredient.name}' created successfully")


@router.put("/{ingredient_id}", response_model=SuccessResponse)
async def update_ingredient(
    ingredient_id: int,
    nutrition: NutritionCreate,
    repo: IngredientRepository = Depends(get_ingredient_repository),
):
    """
    Update an existing ingredient's nutrition values.
    
    Raises:
        NotFoundError: If ingredient not found
    """
    # Update ingredient
    result = repo.update_nutrition(
        ingredient_id=ingredient_id,
        protein_g=nutrition.proteins,
        fat_g=nutrition.fats,
        carbohydrates_g=nutrition.carbohydrates,
    )
    
    if not result:
        raise NotFoundError("Ingredient", str(ingredient_id))
    
    return SuccessResponse(message="Ingredient updated successfully")


@router.delete("/{ingredient_id}", response_model=SuccessResponse)
async def delete_ingredient(
    ingredient_id: int,
    repo: IngredientRepository = Depends(get_ingredient_repository),
):
    """
    Delete an ingredient.
    
    Raises:
        NotFoundError: If ingredient not found
    """
    if not repo.delete(ingredient_id):
        raise NotFoundError("Ingredient", str(ingredient_id))
    
    return SuccessResponse(message="Ingredient deleted successfully")


def _calculate_calories(proteins: float, fats: float, carbohydrates: float) -> float:
    """Calculate calories from macros using 4-9-4 rule."""
    return proteins * 4 + fats * 9 + carbohydrates * 4
