#!/usr/bin/env python3
"""
Nutrition calculation service for calculating dish nutritional information.
"""

from typing import List, Dict
from src.models import Ingredient, NutritionInfo
from src.models.interfaces import NutritionCalculatorInterface


class NutritionCalculator(NutritionCalculatorInterface):
    """
    Service class for calculating nutritional information of dishes.
    
    This class follows the Single Responsibility Principle by encapsulating
    all nutrition calculation logic in one place.
    """
    
    def calculate_total_nutrition_info(
        self, 
        ingredients_nutrition: Dict[str, NutritionInfo], 
        dish_ingredients: Dict[str, float]
    ) -> NutritionInfo:
        """
        Calculate total nutritional information for a dish based on ingredient weights.
        
        Args:
            ingredients_nutrition (Dict[str, NutritionInfo]): Dictionary mapping ingredient names to their nutritional values per 100g
            dish_ingredients (Dict[str, float]): Dictionary mapping ingredient names to their weights in the dish (in grams)
            
        Returns:
            NutritionInfo: Total nutritional values for the dish
        """
        total_nutrition = NutritionInfo(
            calories=0.0,
            fats=0.0,
            proteins=0.0,
            carbohydrates=0.0
        )
        
        for name, weight in dish_ingredients.items():
            nutrition_per_100 = ingredients_nutrition[name]
            total_nutrition.calories += nutrition_per_100.calories * (weight / 100)
            total_nutrition.fats += nutrition_per_100.fats * (weight / 100)
            total_nutrition.proteins += nutrition_per_100.proteins * (weight / 100)
            total_nutrition.carbohydrates += nutrition_per_100.carbohydrates * (weight / 100)
        
        return total_nutrition
