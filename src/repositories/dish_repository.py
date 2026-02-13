"""
Repository for Dish data access.
"""

from typing import List, Optional, Dict
from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import func

from src.repositories.base import BaseRepository
from src.database import Dish, DishIngredient, Ingredient


class DishRepository(BaseRepository[Dish]):
    """
    Repository for Dish CRUD operations.
    Provides data access layer for dishes with ingredients.
    """
    
    @property
    def model(self) -> type[Dish]:
        return Dish
    
    def get_by_id_with_ingredients(self, dish_id: int) -> Optional[Dish]:
        """
        Get dish with loaded ingredients relationship.
        Uses eager loading to avoid N+1 queries.
        
        Args:
            dish_id: ID of dish to retrieve
            
        Returns:
            Dish instance with loaded ingredients or None
        """
        return self.db.query(Dish).options(
            selectinload(Dish.ingredients).selectinload(DishIngredient.ingredient)
        ).filter(Dish.id == dish_id).first()
    
    def get_all_with_ingredients(self, skip: int = 0, limit: int = 100) -> List[Dish]:
        """
        Get all dishes with loaded ingredients.
        Uses eager loading to avoid N+1 queries.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of dishes with loaded ingredients
        """
        return self.db.query(Dish).options(
            selectinload(Dish.ingredients).selectinload(DishIngredient.ingredient)
        ).order_by(Dish.name).offset(skip).limit(limit).all()
    
    def get_by_name(self, name: str) -> Optional[Dish]:
        """
        Get dish by name (case-insensitive).
        
        Args:
            name: Dish name to search for
            
        Returns:
            Dish instance or None if not found
        """
        return self.db.query(Dish).filter(
            func.lower(Dish.name) == name.lower()
        ).first()
    
    def search(self, query: str, limit: int = 20) -> List[Dish]:
        """
        Search dishes by name.
        
        Args:
            query: Search query string
            limit: Maximum number of results
            
        Returns:
            List of matching dishes
        """
        return self.db.query(Dish).filter(
            Dish.name.ilike(f"%{query}%")
        ).options(
            selectinload(Dish.ingredients).selectinload(DishIngredient.ingredient)
        ).limit(limit).all()
    
    def create_dish(self, name: str, ingredients: Dict[str, float]) -> Dish:
        """
        Create a new dish with ingredients.
        
        Args:
            name: Dish name
            ingredients: Dictionary mapping ingredient names to amounts
            
        Returns:
            Created dish instance
            
        Raises:
            ValueError: If any ingredient name doesn't exist
        """
        # Create dish
        dish = Dish(name=name)
        self.db.add(dish)
        self.db.flush()  # Get dish ID
        
        # Add ingredients
        for ing_name, amount in ingredients.items():
            ingredient = self.db.query(Ingredient).filter(
                func.lower(Ingredient.name) == ing_name.lower()
            ).first()
            
            if not ingredient:
                raise ValueError(f"Ingredient '{ing_name}' not found")
            
            dish_ingredient = DishIngredient(
                dish_id=dish.id,
                ingredient_id=ingredient.id,
                amount=amount
            )
            self.db.add(dish_ingredient)
        
        self.db.flush()
        return dish
    
    def update_dish_ingredients(
        self, 
        dish_id: int, 
        ingredients: Dict[str, float]
    ) -> Optional[Dish]:
        """
        Update dish ingredients (replaces all existing ingredients).
        
        Args:
            dish_id: ID of dish to update
            ingredients: Dictionary mapping ingredient names to amounts
            
        Returns:
            Updated dish or None if not found
            
        Raises:
            ValueError: If any ingredient name doesn't exist
        """
        dish = self.get_by_id(dish_id)
        if not dish:
            return None
        
        # Remove existing ingredients
        self.db.query(DishIngredient).filter(
            DishIngredient.dish_id == dish_id
        ).delete()
        
        # Add new ingredients
        for ing_name, amount in ingredients.items():
            ingredient = self.db.query(Ingredient).filter(
                func.lower(Ingredient.name) == ing_name.lower()
            ).first()
            
            if not ingredient:
                raise ValueError(f"Ingredient '{ing_name}' not found")
            
            dish_ingredient = DishIngredient(
                dish_id=dish_id,
                ingredient_id=ingredient.id,
                amount=amount
            )
            self.db.add(dish_ingredient)
        
        self.db.flush()
        return dish
    
    def delete_dish(self, dish_id: int) -> bool:
        """
        Delete a dish and its ingredient associations.
        
        Args:
            dish_id: ID of dish to delete
            
        Returns:
            True if deleted, False if not found
        """
        dish = self.get_by_id(dish_id)
        if not dish:
            return False
        
        # Delete ingredient associations first
        self.db.query(DishIngredient).filter(
            DishIngredient.dish_id == dish_id
        ).delete()
        
        # Delete dish
        self.db.delete(dish)
        self.db.flush()
        return True
    
    def get_dish_ingredients_dict(self, dish_id: int) -> Optional[Dict[str, float]]:
        """
        Get dish ingredients as a dictionary.
        
        Args:
            dish_id: ID of dish
            
        Returns:
            Dictionary mapping ingredient names to amounts, or None if dish not found
        """
        dish = self.get_by_id_with_ingredients(dish_id)
        if not dish:
            return None
        
        return {
            di.ingredient.name: di.amount 
            for di in dish.ingredients 
            if di.ingredient is not None
        }
    
    def name_exists(self, name: str, exclude_id: Optional[int] = None) -> bool:
        """
        Check if dish name already exists.
        
        Args:
            name: Name to check
            exclude_id: Optional ID to exclude from check (for updates)
            
        Returns:
            True if name exists, False otherwise
        """
        query = self.db.query(Dish).filter(
            func.lower(Dish.name) == name.lower()
        )
        if exclude_id:
            query = query.filter(Dish.id != exclude_id)
        return query.first() is not None
    
    def count(self) -> int:
        """Get total count of dishes."""
        return self.db.query(Dish).count()
