#!/usr/bin/env python3
"""
Ingredient data loader service for loading ingredients from database.
"""

from typing import Dict
from src.models import Ingredient, NutritionInfo
from src.models.interfaces import IngredientLoaderInterface
from src.database import get_session, Ingredient as DbIngredient


class IngredientDataLoader(IngredientLoaderInterface):
    """
    Service class for loading ingredient data from database.
    """
    
    def load_ingredients(self) -> Dict[str, Ingredient]:
        """
        Load ingredients from database.
        
        Returns:
            Dict[str, Ingredient]: Dictionary of Ingredient objects loaded from database,
                                   keyed by ingredient name
        """
        session = get_session()
        ingredients = {}
        try:
            for db_ingredient in session.query(DbIngredient).all():
                # Calculate calories (4 kcal/g protein, 9 kcal/g fat, 4 kcal/g carbs)
                calories = (
                    4 * db_ingredient.protein_g +
                    9 * db_ingredient.fat_g +
                    4 * db_ingredient.carbohydrates_g
                )
                
                nutrition = NutritionInfo(
                    proteins=db_ingredient.protein_g,
                    fats=db_ingredient.fat_g,
                    carbohydrates=db_ingredient.carbohydrates_g,
                    calories=calories
                )
                
                ingredient = Ingredient(
                    name=db_ingredient.name,
                    nutrition=nutrition
                )
                ingredients[db_ingredient.name] = ingredient
        finally:
            session.close()
        return ingredients
