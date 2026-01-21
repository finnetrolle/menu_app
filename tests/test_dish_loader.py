"""
Tests for the DishLoader class
"""

import unittest
from unittest.mock import Mock
from src.models.dish_loader import DishLoader
from src.models.ingredient import Ingredient
from src.models.nutrition import NutritionInfo
from src.models.dish import Dish


class TestDishLoader(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create a mock ingredient dictionary
        self.ingredient_dict = {
            "Яйца": Ingredient(
                name="Яйца",
                nutrition=NutritionInfo(
                    calories=155.0,
                    fats=11.0,
                    proteins=13.0,
                    carbohydrates=1.0
                )
            ),
            "Молоко 2.5% жирности": Ingredient(
                name="Молоко 2.5% жирности",
                nutrition=NutritionInfo(
                    calories=42.0,
                    fats=2.5,
                    proteins=3.4,
                    carbohydrates=4.8
                )
            ),
            "Сливочное масло": Ingredient(
                name="Сливочное масло",
                nutrition=NutritionInfo(
                    calories=717.0,
                    fats=81.0,
                    proteins=0.8,
                    carbohydrates=0.1
                )
            )
        }
        
        # Create a temporary directory structure for testing
        import os
        os.makedirs("test_dishes", exist_ok=True)
        
        # Create a test dish file
        test_dish_data = {
            "name": "Тестовый Омлет",
            "ingredients": [
                {"name": "Яйца", "amount": 60},
                {"name": "Молоко 2.5% жирности", "amount": 20},
                {"name": "Сливочное масло", "amount": 2}
            ]
        }
        
        import json
        with open("test_dishes/test_омлет.json", "w", encoding="utf-8") as f:
            json.dump(test_dish_data, f, ensure_ascii=False, indent=2)
    
    def tearDown(self):
        """Clean up after each test method."""
        import os
        import shutil
        if os.path.exists("test_dishes"):
            shutil.rmtree("test_dishes")
    
    def test_load_dishes(self):
        """Test that dishes are loaded correctly from JSON files."""
        # Create DishLoader instance with test directory
        dish_loader = DishLoader(dishes_directory="test_dishes")
        
        # Load dishes
        dishes = dish_loader.load_dishes(self.ingredient_dict)
        
        # Verify we loaded one dish
        self.assertEqual(len(dishes), 1)
        
        # Get the first dish
        dish = dishes[0]
        
        # Verify dish name
        self.assertEqual(dish.name, "Тестовый Омлет")
        
        # Verify ingredients dictionary format
        self.assertIsInstance(dish.ingredients, dict)
        
        # Verify ingredients content
        expected_ingredients = {
            "Яйца": 60,
            "Молоко 2.5% жирности": 20,
            "Сливочное масло": 2
        }
        self.assertEqual(dish.ingredients, expected_ingredients)
    
    def test_load_dishes_with_invalid_ingredient(self):
        """Test that loading fails when an ingredient is not in the dictionary."""
        # Create a dish with an invalid ingredient
        import os
        import json
        
        invalid_dish_data = {
            "name": "Омлет с неправильным ингредиентом",
            "ingredients": [
                {"name": "Яйца", "amount": 60},
                {"name": "Неизвестный ингредиент", "amount": 20}
            ]
        }
        
        with open("test_dishes/invalid_омлет.json", "w", encoding="utf-8") as f:
            json.dump(invalid_dish_data, f, ensure_ascii=False, indent=2)
        
        # Create DishLoader instance with test directory
        dish_loader = DishLoader(dishes_directory="test_dishes")
        
        # Try to load dishes - should raise ValueError
        with self.assertRaises(ValueError) as context:
            dish_loader.load_dishes(self.ingredient_dict)
        
        # Verify the error message
        self.assertIn("Неизвестный ингредиент", str(context.exception))
        
        # Clean up
        os.remove("test_dishes/invalid_омлет.json")
    
    def test_empty_dishes_directory(self):
        """Test loading from empty dishes directory."""
        # Create an empty directory
        import os
        os.makedirs("empty_dishes", exist_ok=True)
        
        dish_loader = DishLoader(dishes_directory="empty_dishes")
        dishes = dish_loader.load_dishes(self.ingredient_dict)
        
        # Should return empty list
        self.assertEqual(len(dishes), 0)
        
        # Clean up
        os.rmdir("empty_dishes")


if __name__ == '__main__':
    unittest.main()
