"""
Interface definitions for the menu application.
These interfaces define contracts that implementations must follow.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from src.models.ingredient import Ingredient
from src.models.dish import Dish
from src.models.nutrition import NutritionInfo


class IngredientLoaderInterface(ABC):
    """Interface for loading ingredient data."""
    
    @abstractmethod
    def load_ingredients(self) -> Dict[str, Ingredient]:
        """Load all ingredients from data source.
        
        Returns:
            Dict[str, Ingredient]: Dictionary of ingredient objects keyed by name
        """
        pass


class DishLoaderInterface(ABC):
    """Interface for loading dish data."""
    
    @abstractmethod
    def load_dishes(self, ingredient_dict: Dict[str, Ingredient]) -> List[Dish]:
        """Load all dishes from data source.
        
        Args:
            ingredient_dict (Dict[str, Ingredient]): Dictionary of existing ingredients
            
        Returns:
            List[Dish]: List of Dish objects
        """
        pass


class NutritionCalculatorInterface(ABC):
    """Interface for calculating nutritional information."""
    
    @abstractmethod
    def calculate_total_nutrition_info(
        self, ingredients_list: List[Ingredient]
    ) -> NutritionInfo:
        """Calculate total nutritional information for a list of ingredients.
        
        Args:
            ingredients_list (List[Ingredient]): List of ingredient objects
            
        Returns:
            NutritionInfo: Object containing total nutritional values
        """
        pass
