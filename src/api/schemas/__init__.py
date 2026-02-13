"""
API schemas package.
Provides Pydantic models for request/response validation.
"""

from .dish import (
    NutritionBase,
    NutritionCreate,
    IngredientBase,
    IngredientCreate,
    IngredientResponse,
    IngredientInDish,
    DishBase,
    DishCreate,
    DishIngredientUpdate,
    DishUpdate,
    DishResponse,
    DishDetailResponse,
    GoalsBase,
    GoalsCreate,
    GoalsResponse,
    SelectedDish,
    MenuProcessRequest,
    IngredientSummary,
    SelectedDishSummary,
    NutritionSummary,
    MenuProcessResponse,
)

from .common import (
    SuccessResponse,
    ErrorResponse,
    DataResponse,
    ListResponse,
    PaginatedRequest,
    APIError,
    NotFoundError,
    ValidationError,
    ConflictError,
    BadRequestError,
)

__all__ = [
    # Dish schemas
    "NutritionBase",
    "NutritionCreate",
    "IngredientBase",
    "IngredientCreate",
    "IngredientResponse",
    "IngredientInDish",
    "DishBase",
    "DishCreate",
    "DishIngredientUpdate",
    "DishUpdate",
    "DishResponse",
    "DishDetailResponse",
    "GoalsBase",
    "GoalsCreate",
    "GoalsResponse",
    "SelectedDish",
    "MenuProcessRequest",
    "IngredientSummary",
    "SelectedDishSummary",
    "NutritionSummary",
    "MenuProcessResponse",
    # Common schemas
    "SuccessResponse",
    "ErrorResponse",
    "DataResponse",
    "ListResponse",
    "PaginatedRequest",
    # Exceptions
    "APIError",
    "NotFoundError",
    "ValidationError",
    "ConflictError",
    "BadRequestError",
]
