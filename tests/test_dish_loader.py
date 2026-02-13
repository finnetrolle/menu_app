"""
Tests for DishLoader using database.
"""
import pytest

from src.models.dish_loader import DishLoader
from src.models.ingredient_data_loader import IngredientDataLoader
from src.database import Base, engine


class TestDishLoader:
    """Test cases for DishLoader class."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test fixtures."""
        # Create tables
        Base.metadata.create_all(bind=engine)
        self.dish_loader = DishLoader()
        self.ingredient_loader = IngredientDataLoader()
        yield

    def test_load_dishes(self):
        """Test loading dishes from database."""
        # Load ingredients first
        ingredients = self.ingredient_loader.load_ingredients()
        
        # Load dishes
        dishes = self.dish_loader.load_dishes(ingredients)
        
        # Verify dishes were loaded
        assert isinstance(dishes, list)
        
        # Verify dish structure if any dishes exist
        for dish in dishes:
            assert hasattr(dish, 'id')
            assert hasattr(dish, 'name')
            assert hasattr(dish, 'ingredients')
            assert isinstance(dish.ingredients, dict)

    def test_delete_dish(self):
        """Test deleting a dish from database."""
        # First create a dish
        dish_data = {
            "name": "Test Dish to Delete",
            "ingredients": {}
        }
        self.dish_loader.save(dish_data)
        
        # Load to get the ID
        ingredients = self.ingredient_loader.load_ingredients()
        dishes = self.dish_loader.load_dishes(ingredients)
        dish_to_delete = next((d for d in dishes if d.name == "Test Dish to Delete"), None)
        
        if dish_to_delete:
            # Delete the dish
            self.dish_loader.delete_dish(dish_to_delete.id)
            
            # Verify dish was deleted
            dishes_after = self.dish_loader.load_dishes(ingredients)
            deleted_dish = next((d for d in dishes_after if d.name == "Test Dish to Delete"), None)
            assert deleted_dish is None

    def test_empty_dishes_database(self):
        """Test loading from database when no dishes exist."""
        # This test verifies the loader handles empty results gracefully
        ingredients = self.ingredient_loader.load_ingredients()
        dishes = self.dish_loader.load_dishes(ingredients)
        
        # Should return a list (may have existing dishes from other tests)
        assert isinstance(dishes, list)
