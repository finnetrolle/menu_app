#!/usr/bin/env python3
"""
Nutrition information model.
"""

from dataclasses import dataclass


@dataclass
class NutritionInfo:
    """
    Represents nutritional information for an ingredient or dish.
    
    Attributes:
        calories (float): Energy content in kilocalories
        fats (float): Fat content in grams
        proteins (float): Protein content in grams
        carbohydrates (float): Carbohydrate content in grams
    """
    calories: float = 0.0
    fats: float = 0.0
    proteins: float = 0.0
    carbohydrates: float = 0.0

    def __init__(self, calories: float = 0.0, fats: float = 0.0, proteins: float = 0.0, carbohydrates: float = 0.0):
        """
        Initialize NutritionInfo object.
        
        Args:
            calories (float): Energy content in kilocalories
            fats (float): Fat content in grams
            proteins (float): Protein content in grams
            carbohydrates (float): Carbohydrate content in grams
        """
        self.calories = calories
        self.fats = fats
        self.proteins = proteins
        self.carbohydrates = carbohydrates
        
    @classmethod
    def from_protein_fat_carb(cls, proteins: float, fats: float, carbohydrates: float):
        """
        Create NutritionInfo object from protein, fat, and carbohydrate values.
        
        Args:
            proteins (float): Protein content in grams
            fats (float): Fat content in grams
            carbohydrates (float): Carbohydrate content in grams
            
        Returns:
            NutritionInfo: Object with calculated calories
        """
        # Calculate calories using standard nutritional values:
        # 1g protein = 4 kcal
        # 1g fat = 9 kcal  
        # 1g carbohydrate = 4 kcal
        calories = proteins * 4 + fats * 9 + carbohydrates * 4
        return cls(calories, fats, proteins, carbohydrates)

    def calculate_calories(self):
        """
        Calculate calories based on protein, fat, and carbohydrate values.
        
        Returns:
            float: Calculated calories (1g protein = 4 kcal, 1g fat = 9 kcal, 1g carbohydrate = 4 kcal)
        """
        return self.proteins * 4 + self.fats * 9 + self.carbohydrates * 4

    def to_dict(self):
        return {
            "calories": self.calories,
            "fats": self.fats,
            "proteins": self.proteins,
            "carbohydrates": self.carbohydrates
        }

    def __str__(self):
        return f"NutritionInfo(calories={self.calories}, fats={self.fats}, proteins={self.proteins}, carbohydrates={self.carbohydrates})"
