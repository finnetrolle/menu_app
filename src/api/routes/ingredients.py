from fastapi import APIRouter, HTTPException, Depends
from typing import List

from src.api.schemas import (
    IngredientResponse,
    IngredientCreate,
    NutritionCreate,
    SuccessResponse,
)
from src.services.ingredient_service import IngredientService
from src.models.ingredient_data_loader import IngredientDataLoader

router = APIRouter(prefix="/ingredients", tags=["ingredients"])


def get_ingredient_service() -> IngredientService:
    """Dependency to get IngredientService instance."""
    ingredient_loader = IngredientDataLoader()
    return IngredientService(ingredient_loader)


@router.get("", response_model=List[IngredientResponse])
async def get_ingredients(service: IngredientService = Depends(get_ingredient_service)):
    """Get all ingredients."""
    return service.get_ingredients()


@router.post("", response_model=SuccessResponse)
async def create_ingredient(
    ingredient: IngredientCreate,
    service: IngredientService = Depends(get_ingredient_service)
):
    """Create a new ingredient."""
    try:
        nutrition_data = {
            "calories": ingredient.nutrition.calories,
            "proteins": ingredient.nutrition.proteins,
            "fats": ingredient.nutrition.fats,
            "carbohydrates": ingredient.nutrition.carbohydrates,
        }
        service.add_ingredient(ingredient.name, nutrition_data)
        return SuccessResponse()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{ingredient_id}", response_model=SuccessResponse)
async def update_ingredient(
    ingredient_id: int,
    nutrition: NutritionCreate,
    service: IngredientService = Depends(get_ingredient_service)
):
    """Update an existing ingredient."""
    try:
        # Get ingredient name by ID
        ingredients_list = service.get_ingredients()
        target = next((item for item in ingredients_list if item["id"] == ingredient_id), None)
        
        if not target:
            raise HTTPException(status_code=404, detail="Ingredient not found")
        
        name = target["name"]
        nutrition_data = {
            "calories": nutrition.calories,
            "proteins": nutrition.proteins,
            "fats": nutrition.fats,
            "carbohydrates": nutrition.carbohydrates,
        }
        service.update_ingredient(name, nutrition_data)
        return SuccessResponse()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{ingredient_id}", response_model=SuccessResponse)
async def delete_ingredient(
    ingredient_id: int,
    service: IngredientService = Depends(get_ingredient_service)
):
    """Delete an ingredient."""
    try:
        # Get ingredient name by ID
        ingredients_list = service.get_ingredients()
        target = next((item for item in ingredients_list if item["id"] == ingredient_id), None)
        
        if not target:
            raise HTTPException(status_code=404, detail="Ingredient not found")
        
        name = target["name"]
        service.delete_ingredient(name)
        return SuccessResponse()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
