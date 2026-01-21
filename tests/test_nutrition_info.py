#!/usr/bin/env python3
"""
Test cases for NutritionInfo class functionality.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models.nutrition import NutritionInfo


def test_nutrition_info_with_all_values():
    """Test creating NutritionInfo with all values provided."""
    nutrition = NutritionInfo(
        calories=500.0,
        fats=20.0,
        proteins=30.0,
        carbohydrates=40.0
    )
    
    assert nutrition.calories == 500.0
    assert nutrition.fats == 20.0
    assert nutrition.proteins == 30.0
    assert nutrition.carbohydrates == 40.0


def test_nutrition_info_from_protein_fat_carb():
    """Test creating NutritionInfo using the new constructor."""
    nutrition = NutritionInfo.from_protein_fat_carb(
        proteins=30.0,
        fats=20.0,
        carbohydrates=40.0
    )
    
    # Expected calories: 30*4 + 20*9 + 40*4 = 120 + 180 + 160 = 460
    assert nutrition.calories == 460.0
    assert nutrition.fats == 20.0
    assert nutrition.proteins == 30.0
    assert nutrition.carbohydrates == 40.0


def test_calculate_calories_method():
    """Test the calculate_calories method."""
    nutrition = NutritionInfo(
        calories=0.0,  # This should be ignored when calculating
        fats=20.0,
        proteins=30.0,
        carbohydrates=40.0
    )
    
    # Expected calories: 30*4 + 20*9 + 40*4 = 120 + 180 + 160 = 460
    calculated_calories = nutrition.calculate_calories()
    assert calculated_calories == 460.0


def test_nutrition_info_default_values():
    """Test creating NutritionInfo with default values."""
    nutrition = NutritionInfo()
    
    assert nutrition.calories == 0.0
    assert nutrition.fats == 0.0
    assert nutrition.proteins == 0.0
    assert nutrition.carbohydrates == 0.0


def main():
    """Run all tests."""
    print("Running NutritionInfo tests...")
    
    test_nutrition_info_with_all_values()
    print("✓ Test 1 passed: Creating NutritionInfo with all values")
    
    test_nutrition_info_from_protein_fat_carb()
    print("✓ Test 2 passed: Creating NutritionInfo from protein/fat/carb")
    
    test_calculate_calories_method()
    print("✓ Test 3 passed: Calculating calories method")
    
    test_nutrition_info_default_values()
    print("✓ Test 4 passed: Default values")
    
    print("\nAll tests passed successfully!")


if __name__ == "__main__":
    main()
