from pydantic import BaseModel, Field
from typing import List, Optional


# Nutrition schemas
class NutritionBase(BaseModel):
    """Base nutrition information."""
    calories: float = Field(..., ge=0, description="Calories per 100g")
    proteins: float = Field(..., ge=0, description="Proteins in grams per 100g")
    fats: float = Field(..., ge=0, description="Fats in grams per 100g")
    carbohydrates: float = Field(..., ge=0, description="Carbohydrates in grams per 100g")


class NutritionCreate(NutritionBase):
    """Schema for creating nutrition info."""
    pass


# Ingredient schemas
class IngredientBase(BaseModel):
    """Base ingredient information."""
    name: str = Field(..., min_length=1, max_length=255)


class IngredientCreate(IngredientBase):
    """Schema for creating an ingredient."""
    nutrition: NutritionCreate


class IngredientResponse(IngredientBase):
    """Schema for ingredient response."""
    id: int
    nutrition: NutritionCreate

    class Config:
        from_attributes = True


class IngredientInDish(BaseModel):
    """Ingredient as part of a dish."""
    name: str
    amount: float = Field(..., gt=0, description="Amount in grams")
    unit: str = "г"
    calories: Optional[float] = None
    proteins: Optional[float] = None
    fats: Optional[float] = None
    carbohydrates: Optional[float] = None


# Dish schemas
class DishBase(BaseModel):
    """Base dish information."""
    name: str = Field(..., min_length=1, max_length=255)


class DishCreate(DishBase):
    """Schema for creating a dish."""
    ingredients: List[IngredientInDish] = []


class DishIngredientUpdate(BaseModel):
    """Schema for updating dish ingredients."""
    name: str
    amount: float = Field(..., gt=0)


class DishUpdate(BaseModel):
    """Schema for updating a dish."""
    ingredients: List[DishIngredientUpdate]


class DishResponse(BaseModel):
    """Schema for dish response."""
    id: int
    name: str
    weight_g: float
    energy_kcal: float
    protein_g: float
    carbohydrates_g: float
    fat_g: float

    class Config:
        from_attributes = True


class DishDetailResponse(BaseModel):
    """Detailed dish response with ingredients."""
    id: int
    name: str
    ingredients: List[IngredientInDish]

    class Config:
        from_attributes = True


# Goal schemas
class GoalsBase(BaseModel):
    """Base goals information."""
    protein: float = Field(0, ge=0)
    fat: float = Field(0, ge=0)
    carbohydrates: float = Field(0, ge=0)
    calories: float = Field(0, ge=0)


class GoalsCreate(GoalsBase):
    """Schema for setting goals."""
    pass


class GoalsResponse(GoalsBase):
    """Schema for goals response."""
    pass


# Menu schemas
class SelectedDish(BaseModel):
    """Selected dish for menu calculation."""
    id: int
    portions: int = Field(1, ge=1)


class MenuProcessRequest(BaseModel):
    """Request for processing menu."""
    dishes: List[SelectedDish]


class IngredientSummary(BaseModel):
    """Summary of ingredient amounts."""
    amount: float
    unit: str = "г"


class SelectedDishSummary(BaseModel):
    """Summary of selected dish."""
    id: int
    name: str
    portions: int


class NutritionSummary(BaseModel):
    """Summary of total nutrition."""
    protein: float
    fat: float
    carbohydrates: float
    calories: float


class MenuProcessResponse(BaseModel):
    """Response for menu processing."""
    dishes: list[SelectedDishSummary]
    ingredients: dict[str, IngredientSummary]
    total_nutrition: NutritionSummary
