"""
Database initialization module.
Loads initial data from JSON files into the database.
"""

import json
import os
from typing import Dict, List

from sqlalchemy import text
from sqlalchemy.orm import Session

from src.database import Base, engine, SessionLocal, Ingredient, Dish, DishIngredient


# Path to data files
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
INGREDIENTS_FILE = os.path.join(DATA_DIR, "ingredients.json")
DISHES_FILE = os.path.join(DATA_DIR, "dishes.json")


def load_ingredients_from_file() -> List[Dict]:
    """Load ingredients data from JSON file."""
    if not os.path.exists(INGREDIENTS_FILE):
        print(f"Ingredients file not found: {INGREDIENTS_FILE}")
        return []
    
    with open(INGREDIENTS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("ingredients", [])


def load_dishes_from_file() -> List[Dict]:
    """Load dishes data from JSON file."""
    if not os.path.exists(DISHES_FILE):
        print(f"Dishes file not found: {DISHES_FILE}")
        return []
    
    with open(DISHES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("dishes", [])


def is_database_empty(session: Session) -> bool:
    """Check if the database has any data."""
    ingredient_count = session.query(Ingredient).count()
    dish_count = session.query(Dish).count()
    return ingredient_count == 0 and dish_count == 0


def populate_ingredients(session: Session, ingredients: List[Dict]) -> int:
    """
    Populate ingredients table with initial data.
    
    Returns:
        Number of ingredients added
    """
    added = 0
    for ing_data in ingredients:
        # Check if ingredient already exists
        existing = session.query(Ingredient).filter_by(name=ing_data["name"]).first()
        if existing:
            continue
        
        ingredient = Ingredient(
            name=ing_data["name"],
            protein_g=ing_data["protein_g"],
            fat_g=ing_data["fat_g"],
            carbohydrates_g=ing_data["carbohydrates_g"]
        )
        session.add(ingredient)
        added += 1
    
    session.commit()
    return added


def populate_dishes(session: Session, dishes: List[Dict]) -> int:
    """
    Populate dishes and dish_ingredients tables with initial data.
    
    Returns:
        Number of dishes added
    """
    added = 0
    for dish_data in dishes:
        # Check if dish already exists
        existing = session.query(Dish).filter_by(name=dish_data["name"]).first()
        if existing:
            continue
        
        dish = Dish(name=dish_data["name"])
        session.add(dish)
        session.flush()  # Get the dish ID
        
        # Add ingredients to the dish
        for ing_name, amount in dish_data.get("ingredients", {}).items():
            ingredient = session.query(Ingredient).filter_by(name=ing_name).first()
            if ingredient:
                dish_ingredient = DishIngredient(
                    dish_id=dish.id,
                    ingredient_id=ingredient.id,
                    amount=amount
                )
                session.add(dish_ingredient)
        
        added += 1
    
    session.commit()
    return added


def init_database(force: bool = False) -> Dict[str, int]:
    """
    Initialize database with initial data from JSON files.
    
    Args:
        force: If True, repopulate even if database is not empty
        
    Returns:
        Dictionary with counts of added items
    """
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    session = SessionLocal()
    try:
        # Check if database is empty or force is True
        if not force and not is_database_empty(session):
            print("Database already contains data. Use force=True to repopulate.")
            return {"ingredients": 0, "dishes": 0}
        
        # Load data from files
        ingredients = load_ingredients_from_file()
        dishes = load_dishes_from_file()
        
        # Populate database
        ingredients_added = populate_ingredients(session, ingredients)
        dishes_added = populate_dishes(session, dishes)
        
        print(f"Database initialized: {ingredients_added} ingredients, {dishes_added} dishes added")
        
        return {
            "ingredients": ingredients_added,
            "dishes": dishes_added
        }
    except Exception as e:
        session.rollback()
        print(f"Error initializing database: {e}")
        raise
    finally:
        session.close()


def check_database_connection() -> bool:
    """Check if database connection is working."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"Database connection error: {e}")
        return False


if __name__ == "__main__":
    # Run initialization when called directly
    init_database()
