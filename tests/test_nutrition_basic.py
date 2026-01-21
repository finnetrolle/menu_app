#!/usr/bin/env python3
"""
Basic test to ensure existing functionality still works.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models.nutrition import NutritionInfo


def test_existing_functionality():
    """Test that existing functionality still works."""
    
    # Test creating NutritionInfo with all values (existing functionality)
    nutrition_info = NutritionInfo(
        calories=100.0,
        fats=5.0,
        proteins=10.0,
        carbohydrates=20.0
    )
    
    assert nutrition_info.calories == 100.0
    assert nutrition_info.fats == 5.0
    assert nutrition_info.proteins == 10.0
    assert nutrition_info.carbohydrates == 20.0
    
    # Test default values (existing functionality)
    nutrition_default = NutritionInfo()
    assert nutrition_default.calories == 0.0
    assert nutrition_default.fats == 0.0
    assert nutrition_default.proteins == 0.0
    assert nutrition_default.carbohydrates == 0.0
    
    # Test string representation (existing functionality)
    str_repr = str(nutrition_info)
    assert "NutritionInfo" in str_repr
    assert "calories=100.0" in str_repr
    
    print("✓ All existing functionality tests passed")


def test_new_functionality():
    """Test new functionality."""
    
    # Test the new constructor method
    nutrition_from_values = NutritionInfo.from_protein_fat_carb(
        proteins=30.0,
        fats=20.0,
        carbohydrates=40.0
    )
    
    # Expected calories: 30*4 + 20*9 + 40*4 = 120 + 180 + 160 = 460
    assert nutrition_from_values.calories == 460.0
    assert nutrition_from_values.fats == 20.0
    assert nutrition_from_values.proteins == 30.0
    assert nutrition_from_values.carbohydrates == 40.0
    
    # Test calculate_calories method
    nutrition_for_calc = NutritionInfo(
        calories=0.0,  # This should be ignored in calculation
        fats=20.0,
        proteins=30.0,
        carbohydrates=40.0
    )
    
    calculated = nutrition_for_calc.calculate_calories()
    assert calculated == 460.0
    
    print("✓ All new functionality tests passed")


if __name__ == "__main__":
    test_existing_functionality()
    test_new_functionality()
    print("\nAll tests passed successfully!")
