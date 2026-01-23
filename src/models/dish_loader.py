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
