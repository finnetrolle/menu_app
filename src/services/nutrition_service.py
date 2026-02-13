"""
Nutrition service for calculating dish nutrition.
Separates business logic from data access.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass

from src.repositories import DishRepository, IngredientRepository
from src.database import Dish, DishIngredient


@dataclass
class NutritionInfo:
    """Nutrition information data class."""
    calories: float = 0.0
    proteins: float = 0.0
    fats: float = 0.0
    carbohydrates: float = 0.0
    
    @classmethod
    def from_macros(cls, proteins: float, fats: float, carbohydrates: float) -> "NutritionInfo":
        """Calculate calories from macros (4-9-4 rule)."""
        calories = proteins * 4 + fats * 9 + carbohydrates * 4
        return cls(calories=calories, proteins=proteins, fats=fats, carbohydrates=carbohydrates)
    
    def multiply(self, factor: float) -> "NutritionInfo":
        """Multiply all values by a factor."""
        return NutritionInfo(
            calories=self.calories * factor,
            proteins=self.proteins * factor,
            fats=self.fats * factor,
            carbohydrates=self.carbohydrates * factor,
        )
    
    def add(self, other: "NutritionInfo") -> "NutritionInfo":
        """Add another NutritionInfo to this one."""
        return NutritionInfo(
            calories=self.calories + other.calories,
            proteins=self.proteins + other.proteins,
            fats=self.fats + other.fats,
            carbohydrates=self.carbohydrates + other.carbohydrates,
        )


class NutritionService:
    """
    Service for calculating nutrition information.
    Uses repositories for data access.
    """
    
    def __init__(
        self,
        dish_repo: DishRepository,
        ingredient_repo: IngredientRepository
    ):
        """
        Initialize nutrition service.
        
        Args:
            dish_repo: Repository for dish data access
            ingredient_repo: Repository for ingredient data access
        """
        self.dish_repo = dish_repo
        self.ingredient_repo = ingredient_repo
    
    def get_ingredient_nutrition(self, ingredient_name: str) -> Optional[NutritionInfo]:
        """
        Get nutrition info for an ingredient per 100g.
        
        Args:
            ingredient_name: Name of the ingredient
            
        Returns:
            NutritionInfo or None if not found
        """
        ingredient = self.ingredient_repo.get_by_name(ingredient_name)
        if not ingredient:
            return None
        
        return NutritionInfo.from_macros(
            proteins=ingredient.protein_g,
            fats=ingredient.fat_g,
            carbohydrates=ingredient.carbohydrates_g
        )
    
    def calculate_ingredient_nutrition(
        self, 
        ingredient_name: str, 
        amount_g: float
    ) -> Optional[NutritionInfo]:
        """
        Calculate nutrition for a specific amount of ingredient.
        
        Args:
            ingredient_name: Name of the ingredient
            amount_g: Amount in grams
            
        Returns:
            NutritionInfo scaled to the amount, or None if ingredient not found
        """
        base_nutrition = self.get_ingredient_nutrition(ingredient_name)
        if not base_nutrition:
            return None
        
        # Scale by amount (nutrition is per 100g)
        factor = amount_g / 100
        return base_nutrition.multiply(factor)
    
    def calculate_dish_nutrition(
        self, 
        dish_id: int
    ) -> Optional[Dict]:
        """
        Calculate total nutrition for a dish.
        
        Args:
            dish_id: ID of the dish
            
        Returns:
            Dictionary with dish data and nutrition, or None if not found
        """
        dish = self.dish_repo.get_by_id_with_ingredients(dish_id)
        if not dish:
            return None
        
        total_nutrition = NutritionInfo()
        total_weight = 0.0
        
        for di in dish.ingredients:
            if di.ingredient:
                ing_nutrition = self.calculate_ingredient_nutrition(
                    di.ingredient.name, 
                    di.amount
                )
                if ing_nutrition:
                    total_nutrition = total_nutrition.add(ing_nutrition)
                total_weight += di.amount
        
        return {
            "id": dish.id,
            "name": dish.name,
            "weight_g": round(total_weight, 2),
            "energy_kcal": round(total_nutrition.calories, 2),
            "protein_g": round(total_nutrition.proteins, 2),
            "fat_g": round(total_nutrition.fats, 2),
            "carbohydrates_g": round(total_nutrition.carbohydrates, 2),
        }
    
    def get_dishes_with_nutrition(
        self, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Dict]:
        """
        Get all dishes with calculated nutrition.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of dishes with nutrition data
        """
        dishes = self.dish_repo.get_all_with_ingredients(skip=skip, limit=limit)
        result = []
        
        for dish in dishes:
            dish_data = self._calculate_dish_nutrition_from_model(dish)
            if dish_data:
                result.append(dish_data)
        
        # Sort by name
        result.sort(key=lambda x: x["name"].lower())
        return result
    
    def get_dish_with_ingredients(self, dish_id: int) -> Optional[Dict]:
        """
        Get dish details with ingredient nutrition.
        
        Args:
            dish_id: ID of the dish
            
        Returns:
            Dictionary with dish data and ingredient details, or None if not found
        """
        dish = self.dish_repo.get_by_id_with_ingredients(dish_id)
        if not dish:
            return None
        
        ingredients_list = []
        
        for di in dish.ingredients:
            if di.ingredient:
                nutrition = self.calculate_ingredient_nutrition(
                    di.ingredient.name, 
                    di.amount
                )
                
                ingredient_data = {
                    "name": di.ingredient.name,
                    "amount": di.amount,
                    "unit": "г",
                }
                
                if nutrition:
                    ingredient_data.update({
                        "calories": round(nutrition.calories, 2),
                        "proteins": round(nutrition.proteins, 2),
                        "fats": round(nutrition.fats, 2),
                        "carbohydrates": round(nutrition.carbohydrates, 2),
                    })
                
                ingredients_list.append(ingredient_data)
        
        return {
            "id": dish.id,
            "name": dish.name,
            "ingredients": ingredients_list,
        }
    
    def calculate_menu_nutrition(
        self, 
        selected_dishes: List[Dict]
    ) -> Dict:
        """
        Calculate total nutrition for a menu selection.
        
        Args:
            selected_dishes: List of dicts with dish_id and portions
            
        Returns:
            Dictionary with total nutrition
        """
        total = NutritionInfo()
        
        for selection in selected_dishes:
            dish_id = selection.get("id")
            portions = selection.get("portions", 1)
            
            dish_data = self.calculate_dish_nutrition(dish_id)
            if dish_data:
                portion_nutrition = NutritionInfo(
                    calories=dish_data["energy_kcal"],
                    proteins=dish_data["protein_g"],
                    fats=dish_data["fat_g"],
                    carbohydrates=dish_data["carbohydrates_g"],
                )
                total = total.add(portion_nutrition.multiply(portions))
        
        return {
            "calories": round(total.calories, 2),
            "protein": round(total.proteins, 2),
            "fat": round(total.fats, 2),
            "carbohydrates": round(total.carbohydrates, 2),
        }
    
    def _calculate_dish_nutrition_from_model(self, dish: Dish) -> Optional[Dict]:
        """
        Calculate nutrition from a Dish model instance.
        
        Args:
            dish: Dish model with loaded ingredients
            
        Returns:
            Dictionary with dish data and nutrition
        """
        total_nutrition = NutritionInfo()
        total_weight = 0.0
        
        for di in dish.ingredients:
            if di.ingredient:
                ing_nutrition = self.calculate_ingredient_nutrition(
                    di.ingredient.name, 
                    di.amount
                )
                if ing_nutrition:
                    total_nutrition = total_nutrition.add(ing_nutrition)
                total_weight += di.amount
        
        return {
            "id": dish.id,
            "name": dish.name,
            "weight_g": round(total_weight, 2),
            "energy_kcal": round(total_nutrition.calories, 2),
            "protein_g": round(total_nutrition.proteins, 2),
            "fat_g": round(total_nutrition.fats, 2),
            "carbohydrates_g": round(total_nutrition.carbohydrates, 2),
        }
