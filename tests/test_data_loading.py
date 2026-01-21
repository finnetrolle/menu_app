"""
Тесты для проверки корректной загрузки данных
"""

import unittest
from unittest.mock import patch, mock_open
import os
import sys

# Добавляем путь к приложению в системный путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")

from src.models.ingredient_data_loader import IngredientDataLoader
from src.models.dish_loader import DishLoader

class TestDataLoading(unittest.TestCase):
    
    def test_load_ingredients_from_csv(self):
        """Тест загрузки данных ингредиентов из CSV файла"""
        loader = IngredientDataLoader()
        ingredients = loader.load_ingredients()
        self.assertGreater(len(ingredients), 0)
    
    def test_load_dishes_from_json(self):
        """Тест загрузки данных о блюдах из JSON файлов"""
        from src.models.ingredient_data_loader import IngredientDataLoader
        ingredient_loader = IngredientDataLoader()
        ingredient_dict = ingredient_loader.load_ingredients()
        loader = DishLoader("dishes")
        dishes = loader.load_dishes(ingredient_dict)
        self.assertGreater(len(dishes), 0)
    
    # validate_data_files больше не существует, проверка интегрирована в методы загрузки
    def test_ingredients_csv_structure(self):
        """Тест структуры CSV файла с ингредиентами"""
        # Проверяем, что файл существует
        self.assertTrue(os.path.exists("data/ingredients.csv"))
        
        # Читаем CSV файл
        with open("data/ingredients.csv", "r", encoding="utf-8") as f:
            content = f.read()
            
        # Проверяем наличие заголовков
        self.assertIn("name", content)
        self.assertIn("protein_g", content)
        self.assertIn("fat_g", content)
        self.assertIn("carbohydrates_g", content)
        self.assertIn("protein_g", content)
        self.assertIn("carbohydrates_g", content)
        self.assertIn("fat_g", content)
        
    def test_dish_files_exist(self):
        """Тест наличия файлов блюд"""
        # Проверяем, что папка dishes существует
        self.assertTrue(os.path.exists("dishes/"))
        
        # Проверяем наличие файлов блюд
        dish_files = os.listdir("dishes/")
        self.assertGreater(len(dish_files), 0)
        
        # Проверяем, что файлы имеют расширение .json
        for file in dish_files:
            self.assertTrue(file.endswith(".json"))

if __name__ == '__main__':
    unittest.main()
