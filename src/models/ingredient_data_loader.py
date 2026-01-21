#!/usr/bin/env python3
"""
Ingredient data loader service for loading ingredients from CSV files.
"""

import csv
from typing import Dict
from src.models import Ingredient, NutritionInfo
from src.models.interfaces import IngredientLoaderInterface


class IngredientDataLoader(IngredientLoaderInterface):
    """
    Service class for loading ingredient data from CSV files.
    
    This class follows the Single Responsibility Principle by encapsulating
    all ingredient data loading logic in one place.
    """
    
    def load_ingredients(self) -> Dict[str, Ingredient]:
        """
        Load ingredients from a CSV file.
        
        Returns:
            Dict[str, Ingredient]: Dictionary of Ingredient objects loaded from the CSV file,
                                   keyed by ingredient name
            
        Raises:
            FileNotFoundError: If the specified CSV file does not exist
            Exception: If there's an error during CSV parsing or data conversion
        """
        ingredients = {}
        
        try:
            with open("data/ingredients.csv", 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                # Create dictionary of ingredients from CSV data, using name as key
                for row in reader:
                    # Handle empty values by converting them to 0.0
                    protein_g = row["protein_g"].strip()
                    fat_g = row["fat_g"].strip()
                    carbohydrates_g = row["carbohydrates_g"].strip()
                    
                    # Convert to float, handling empty strings
                    protein_value = float(protein_g) if protein_g else 0.0
                    fat_value = float(fat_g) if fat_g else 0.0
                    carbohydrates_value = float(carbohydrates_g) if carbohydrates_g else 0.0
                    
                    ingredient = Ingredient(
                        name=row["name"],
                        nutrition = NutritionInfo.from_protein_fat_carb(protein_value, fat_value, carbohydrates_value)
                    )
                    ingredients[row["name"]] = ingredient
                    
        except FileNotFoundError:
            raise FileNotFoundError("Ingredient CSV file not found: data/ingredients.csv")
        except Exception as e:
            raise Exception(f"Error loading ingredients from CSV file: {e}")
        
        return ingredients
