"""
Module for loading dishes from JSON files.
"""

import os
import json
from typing import Dict, List
from src.models.dish import Dish
from src.models.ingredient import Ingredient
from src.models.interfaces import DishLoaderInterface


class DishLoader(DishLoaderInterface):
    """
    Class for loading dishes from JSON files in the dishes directory.
    Each dish is a separate JSON file containing name and ingredients.
    """
    
    def __init__(self, dishes_directory: str = "dishes"):
        """
        Initialize the DishLoader.
        
        Args:
            dishes_directory (str): Path to the directory containing dish JSON files
        """
        self.dishes_directory = dishes_directory
        
    def load_dishes(self, ingredient_dict: Dict[str, Ingredient]) -> List[Dish]:
        """
        Load all dishes from JSON files in the dishes directory.
        
        Args:
            ingredient_dict (Dict[str, Ingredient]): Dictionary of existing ingredients
            
        Returns:
            List[Dish]: List of Dish objects
            
        Raises:
            FileNotFoundError: If the dishes directory doesn't exist
            json.JSONDecodeError: If a dish file is not valid JSON
        """
        # Check if dishes directory exists
        if not os.path.exists(self.dishes_directory):
            raise FileNotFoundError(f"Dishes directory '{self.dishes_directory}' not found")
            
        dishes = []
        
        # Iterate through all files in the dishes directory
        for filename in os.listdir(self.dishes_directory):
            if filename.endswith('.json'):
                file_path = os.path.join(self.dishes_directory, filename)
                
                # Load dish data from JSON file
                with open(file_path, 'r', encoding='utf-8') as f:
                    dish_data = json.load(f)
                
                # Convert ingredients from list format to dictionary format
                # Each ingredient in the list has "name" and "amount" fields
                ingredients_dict = {}
                for ingredient in dish_data.get('ingredients', []):
                    ingredient_name = ingredient['name']
                    weight = ingredient['amount']
                    
                    # Validate that this ingredient exists in ingredient_dict
                    if ingredient_name not in ingredient_dict:
                        raise ValueError(f"Ingredient '{ingredient_name}' in dish '{filename}' is not in the ingredient dictionary")
                    
                    ingredients_dict[ingredient_name] = weight
                
                # Create Dish object with the required dictionary format
                dish = Dish(
                    id=dish_data.get('id', 0),
                    name=dish_data['name'],
                    ingredients=ingredients_dict
                )
                
                dishes.append(dish)
                
        return dishes

    def save(self, dish_data: dict):
        """
        Save a dish to a JSON file in the dishes directory.
        
        Args:
            dish_data (dict): Dictionary containing 'name' and 'ingredients'
        """
        # Convert ingredients dict to list format expected by JSON
        ingredients_list = [
            {"name": name, "amount": amount} 
            for name, amount in dish_data["ingredients"].items()
        ]
        
        # Create dish data for JSON
        dish_json = {
            "name": dish_data["name"],
            "ingredients": ingredients_list
        }
        
        # Generate filename from dish name
        filename = f"{dish_data['name']}.json"
        file_path = os.path.join(self.dishes_directory, filename)
        
        # Write to file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(dish_json, f, ensure_ascii=False, indent=2)
