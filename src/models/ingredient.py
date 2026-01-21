#!/usr/bin/env python3
"""
Ingredient model with nutrition information.
"""

from dataclasses import dataclass
from src.models.nutrition import NutritionInfo


@dataclass
class Ingredient:
    """
    Represents an ingredient with its name and nutritional information.
    
    Attributes:
        name (str): Name of the ingredient
        nutrition (NutritionInfo): Nutritional information for the ingredient
    """
    name: str
    nutrition: NutritionInfo

    def __str__(self):
        return f"Ingredient(name='{self.name}', nutrition={self.nutrition})"

    def to_dict(self):
        return {
            "name": self.name,
            "nutrition": self.nutrition.to_dict()
        }
