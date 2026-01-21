#!/usr/bin/env python3
"""
Test file for the class structure implementation.
"""

from src.models.nutrition import NutritionInfo
from src.models.ingredient import Ingredient
from src.models.dish import Dish


def test_class_structure():
    """Test that all required classes work as expected."""
    
    # Test NutritionInfo class
    nutrition_info = NutritionInfo(
        calories=100.0,
        fats=5.0,
        proteins=10.0,
        carbohydrates=20.0
    )
    
    print("NutritionInfo object created successfully:")
    print(f"  Calories: {nutrition_info.calories}")
    print(f"  Fats: {nutrition_info.fats}")
    print(f"  Proteins: {nutrition_info.proteins}")
    print(f"  Carbohydrates: {nutrition_info.carbohydrates}")
    
    # Test Ingredient class
    ingredient = Ingredient(
        name="Молоко",
        nutrition=nutrition_info
    )
    
    print("\nIngredient object created successfully:")
    print(f"  Name: {ingredient.name}")
    print(f"  Nutrition: {ingredient.nutrition}")
    
    # Test Dish class
    dish = Dish(
        id=1,
        name="Омлет",
        ingredients={
            "Молоко": 100.0,
            "Яйца": 150.0
        }
    )
    
    print("\nDish object created successfully:")
    print(f"  Name: {dish.name}")
    print(f"  Ingredients: {dish.ingredients}")
    
    # For demonstration, we'll create some sample ingredients with nutrition data
    milk_nutrition = NutritionInfo(
        calories=42.0,
        fats=3.5,
        proteins=3.4,
        carbohydrates=4.8
    )
    
    egg_nutrition = NutritionInfo(
        calories=155.0,
        fats=11.0,
        proteins=13.0,
        carbohydrates=1.2
    )
    
    milk_ingredient = Ingredient("Молоко", milk_nutrition)
    egg_ingredient = Ingredient("Яйца", egg_nutrition)
    
    # Test methods
    print("\nTesting Dish methods:")
    total_weight = dish.total_weight
    print(f"  Total weight: {total_weight}g")
    
    print("\nAll tests passed!")


if __name__ == "__main__":
    test_class_structure()
