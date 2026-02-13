"""
Repository for Ingredient data access.
"""

from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from sqlalchemy import func

from src.repositories.base import BaseRepository
from src.database import Ingredient


class IngredientRepository(BaseRepository[Ingredient]):
    """
    Repository for Ingredient CRUD operations.
    Provides data access layer for ingredients.
    """
    
    @property
    def model(self) -> type[Ingredient]:
        return Ingredient
    
    def get_by_name(self, name: str) -> Optional[Ingredient]:
        """
        Get ingredient by name (case-insensitive).
        
        Args:
            name: Ingredient name to search for
            
        Returns:
            Ingredient instance or None if not found
        """
        return self.db.query(Ingredient).filter(
            func.lower(Ingredient.name) == name.lower()
        ).first()
    
    def search(self, query: str, limit: int = 20) -> List[Ingredient]:
        """
        Search ingredients by name.
        
        Args:
            query: Search query string
            limit: Maximum number of results
            
        Returns:
            List of matching ingredients
        """
        return self.db.query(Ingredient).filter(
            Ingredient.name.ilike(f"%{query}%")
        ).limit(limit).all()
    
    def get_all_sorted(self, skip: int = 0, limit: int = 100) -> List[Ingredient]:
        """
        Get all ingredients sorted by name.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of ingredients sorted alphabetically
        """
        return self.db.query(Ingredient).order_by(
            Ingredient.name
        ).offset(skip).limit(limit).all()
    
    def create_ingredient(
        self, 
        name: str, 
        protein_g: float, 
        fat_g: float, 
        carbohydrates_g: float
    ) -> Ingredient:
        """
        Create a new ingredient.
        
        Args:
            name: Ingredient name
            protein_g: Protein content per 100g
            fat_g: Fat content per 100g
            carbohydrates_g: Carbohydrates content per 100g
            
        Returns:
            Created ingredient instance
        """
        ingredient = Ingredient(
            name=name,
            protein_g=protein_g,
            fat_g=fat_g,
            carbohydrates_g=carbohydrates_g
        )
        return self.create(ingredient)
    
    def update_nutrition(
        self, 
        ingredient_id: int, 
        protein_g: float, 
        fat_g: float, 
        carbohydrates_g: float
    ) -> Optional[Ingredient]:
        """
        Update ingredient nutrition values.
        
        Args:
            ingredient_id: ID of ingredient to update
            protein_g: New protein content per 100g
            fat_g: New fat content per 100g
            carbohydrates_g: New carbohydrates content per 100g
            
        Returns:
            Updated ingredient or None if not found
        """
        ingredient = self.get_by_id(ingredient_id)
        if ingredient:
            ingredient.protein_g = protein_g
            ingredient.fat_g = fat_g
            ingredient.carbohydrates_g = carbohydrates_g
            self.db.flush()
            return ingredient
        return None
    
    def get_nutrition_dict(self) -> Dict[str, Dict[str, float]]:
        """
        Get all ingredients as a nutrition dictionary.
        
        Returns:
            Dictionary mapping ingredient names to nutrition values
            Example: {"Chicken": {"protein_g": 25, "fat_g": 5, "carbohydrates_g": 0}}
        """
        ingredients = self.db.query(Ingredient).all()
        return {
            ing.name: {
                "protein_g": ing.protein_g,
                "fat_g": ing.fat_g,
                "carbohydrates_g": ing.carbohydrates_g
            }
            for ing in ingredients
        }
    
    def name_exists(self, name: str, exclude_id: Optional[int] = None) -> bool:
        """
        Check if ingredient name already exists.
        
        Args:
            name: Name to check
            exclude_id: Optional ID to exclude from check (for updates)
            
        Returns:
            True if name exists, False otherwise
        """
        query = self.db.query(Ingredient).filter(
            func.lower(Ingredient.name) == name.lower()
        )
        if exclude_id:
            query = query.filter(Ingredient.id != exclude_id)
        return query.first() is not None
