"""
Repository pattern implementation for data access layer.
Provides clean separation between business logic and database operations.
"""

from src.repositories.base import BaseRepository
from src.repositories.dish_repository import DishRepository
from src.repositories.ingredient_repository import IngredientRepository

__all__ = [
    "BaseRepository",
    "DishRepository",
    "IngredientRepository",
]
