"""
Module for loading dishes from database.
"""

from typing import Dict, List
from src.models.dish import Dish
from src.models.ingredient import Ingredient
from src.models.interfaces import DishLoaderInterface
from src.database import get_session, Dish as DbDish, DishIngredient, Ingredient as DbIngredient

class DishLoader(DishLoaderInterface):
    """
    Class for loading dishes from database.
    """
    
    def __init__(self):
        """
        Initialize the DishLoader.
        """
        pass
        
    def load_dishes(self, ingredient_dict: Dict[str, Ingredient]) -> List[Dish]:
        """
        Load all dishes from database.
        
        Args:
            ingredient_dict (Dict[str, Ingredient]): Dictionary of existing ingredients
            
        Returns:
            List[Dish]: List of Dish objects
        """
        session = get_session()
        dishes = []
        try:
            for db_dish in session.query(DbDish).all():
                ingredients = {}
                for di in db_dish.ingredients:
                    # Проверяем, что ингредиент существует перед доступом к его атрибутам
                    if di.ingredient is not None:
                        ingredients[di.ingredient.name] = di.amount
                dish = Dish(
                    id=db_dish.id,
                    name=db_dish.name,
                    ingredients=ingredients
                )
                dishes.append(dish)
        finally:
            session.close()
        return dishes

    def save(self, dish_data: dict):
        """
        Save a dish to the database.
        
        Args:
            dish_data (dict): Dictionary containing 'name' and 'ingredients'
        """
        session = get_session()
        try:
            # Check if dish exists by name
            db_dish = session.query(DbDish).filter_by(name=dish_data['name']).first()
            if not db_dish:
                db_dish = DbDish(name=dish_data['name'])
                session.add(db_dish)
                session.flush()
            
            # Clear existing ingredients
            session.query(DishIngredient).filter_by(dish_id=db_dish.id).delete()
            
            # Add new ingredients
            for name, amount in dish_data['ingredients'].items():
                db_ingredient = session.query(DbIngredient).filter_by(name=name).first()
                if db_ingredient:
                    dish_ing = DishIngredient(
                        dish_id=db_dish.id,
                        ingredient_id=db_ingredient.id,
                        amount=amount
                    )
                    session.add(dish_ing)
            
            session.commit()
        finally:
            session.close()

    def delete_dish(self, dish_id: int):
        """
        Удаляет блюдо из базы данных по ID.
        
        Args:
            dish_id: ID блюда
        """
        session = get_session()
        try:
            # Удаляем связанные ингредиенты
            session.query(DishIngredient).filter_by(dish_id=dish_id).delete()
            # Удаляем само блюдо
            session.query(DbDish).filter_by(id=dish_id).delete()
            session.commit()
        finally:
            session.close()

    def get_dish_by_id(self, dish_id: int):
        """
        Получает блюдо из базы данных по ID.
        
        Args:
            dish_id: ID блюда
            
        Returns:
            Dish object with nutrition info or None if not found
        """
        from src.models.ingredient_data_loader import IngredientDataLoader
        from src.models.nutrition_calculator import NutritionCalculator
        
        session = get_session()
        try:
            db_dish = session.query(DbDish).filter_by(id=dish_id).first()
            if not db_dish:
                return None
            
            # Load ingredients and calculate nutrition
            ingredient_loader = IngredientDataLoader()
            nutrition_calculator = NutritionCalculator()
            
            ingredients_dict = {}
            for di in db_dish.ingredients:
                if di.ingredient is not None:
                    ingredients_dict[di.ingredient.name] = di.amount
            
            # Create dish with nutrition info
            dish = Dish(
                id=db_dish.id,
                name=db_dish.name,
                ingredients=ingredients_dict
            )
            
            # Calculate nutrition for the dish
            # load_ingredients returns Dict[str, Ingredient], but calculate_total_nutrition_info
            # expects Dict[str, NutritionInfo], so we need to convert
            ingredients = ingredient_loader.load_ingredients()
            ingredients_nutrition = {name: ing.nutrition for name, ing in ingredients.items()}
            nutrition_info = nutrition_calculator.calculate_total_nutrition_info(ingredients_nutrition, ingredients_dict)
            
            # Add nutrition attributes to dish
            dish.energy_kcal = nutrition_info.calories
            dish.protein_g = nutrition_info.proteins
            dish.fat_g = nutrition_info.fats
            dish.carbohydrates_g = nutrition_info.carbohydrates
            dish.weight_g = sum(ingredients_dict.values())
            
            return dish
        finally:
            session.close()
