"""
API endpoint tests for FastAPI application.
Tests all CRUD operations and business logic.
"""

import pytest
from fastapi.testclient import TestClient


class TestHealthEndpoints:
    """Tests for health and root endpoints."""
    
    def test_root_endpoint(self, client: TestClient):
        """Test root endpoint returns API info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "docs" in data
        assert data["docs"] == "/docs"
    
    def test_health_check(self, client: TestClient):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestIngredientEndpoints:
    """Tests for ingredient CRUD operations."""
    
    def test_get_ingredients_empty(self, client: TestClient):
        """Test getting ingredients when database is empty."""
        response = client.get("/api/ingredients")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_create_ingredient(self, client: TestClient, sample_ingredient_data):
        """Test creating a new ingredient."""
        response = client.post("/api/ingredients", json=sample_ingredient_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
    
    def test_create_duplicate_ingredient(self, client: TestClient, sample_ingredient_data):
        """Test that creating duplicate ingredient fails."""
        # Create first ingredient
        client.post("/api/ingredients", json=sample_ingredient_data)
        
        # Try to create duplicate
        response = client.post("/api/ingredients", json=sample_ingredient_data)
        assert response.status_code == 409  # Conflict
    
    def test_get_ingredients_after_create(self, client: TestClient, sample_ingredient_data):
        """Test getting ingredients after creating one."""
        # Create ingredient
        client.post("/api/ingredients", json=sample_ingredient_data)
        
        # Get all ingredients
        response = client.get("/api/ingredients")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == sample_ingredient_data["name"]
    
    def test_update_ingredient(self, client: TestClient, sample_ingredient_data):
        """Test updating an ingredient."""
        # Create ingredient
        client.post("/api/ingredients", json=sample_ingredient_data)
        
        # Get ingredient ID
        response = client.get("/api/ingredients")
        ingredient_id = response.json()[0]["id"]
        
        # Update ingredient
        update_data = {
            "calories": 200,
            "proteins": 20,
            "fats": 10,
            "carbohydrates": 30
        }
        response = client.put(f"/api/ingredients/{ingredient_id}", json=update_data)
        assert response.status_code == 200
    
    def test_update_nonexistent_ingredient(self, client: TestClient):
        """Test updating a non-existent ingredient."""
        update_data = {
            "calories": 200,
            "proteins": 20,
            "fats": 10,
            "carbohydrates": 30
        }
        response = client.put("/api/ingredients/999", json=update_data)
        assert response.status_code == 404
    
    def test_delete_ingredient(self, client: TestClient, sample_ingredient_data):
        """Test deleting an ingredient."""
        # Create ingredient
        client.post("/api/ingredients", json=sample_ingredient_data)
        
        # Get ingredient ID
        response = client.get("/api/ingredients")
        ingredient_id = response.json()[0]["id"]
        
        # Delete ingredient
        response = client.delete(f"/api/ingredients/{ingredient_id}")
        assert response.status_code == 200
        
        # Verify deletion
        response = client.get("/api/ingredients")
        assert len(response.json()) == 0
    
    def test_delete_nonexistent_ingredient(self, client: TestClient):
        """Test deleting a non-existent ingredient."""
        response = client.delete("/api/ingredients/999")
        assert response.status_code == 404


class TestDishEndpoints:
    """Tests for dish CRUD operations."""
    
    def test_get_dishes_empty(self, client: TestClient):
        """Test getting dishes when database is empty."""
        response = client.get("/api/dishes")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_create_dish(self, client: TestClient, sample_dish_data, sample_ingredient_data):
        """Test creating a new dish."""
        # Create ingredient first
        client.post("/api/ingredients", json=sample_ingredient_data)
        
        # Create dish
        response = client.post("/api/dishes/new", json=sample_dish_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
    
    def test_create_dish_without_ingredients(self, client: TestClient):
        """Test that creating dish without ingredients fails."""
        dish_data = {"name": "Empty Dish", "ingredients": []}
        response = client.post("/api/dishes/new", json=dish_data)
        assert response.status_code == 400
    
    def test_create_dish_with_nonexistent_ingredient(self, client: TestClient):
        """Test that creating dish with non-existent ingredient fails."""
        dish_data = {
            "name": "Invalid Dish",
            "ingredients": [{"name": "Nonexistent", "amount": 100}]
        }
        response = client.post("/api/dishes/new", json=dish_data)
        assert response.status_code == 400
    
    def test_get_dish_by_id(self, client: TestClient, sample_dish_data, sample_ingredient_data):
        """Test getting a dish by ID."""
        # Create ingredient and dish
        client.post("/api/ingredients", json=sample_ingredient_data)
        client.post("/api/dishes/new", json=sample_dish_data)
        
        # Get dish ID
        response = client.get("/api/dishes")
        dish_id = response.json()[0]["id"]
        
        # Get dish by ID
        response = client.get(f"/api/dishes/{dish_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == sample_dish_data["name"]
        assert "ingredients" in data
    
    def test_get_nonexistent_dish(self, client: TestClient):
        """Test getting a non-existent dish."""
        response = client.get("/api/dishes/999")
        assert response.status_code == 404
    
    def test_update_dish(self, client: TestClient, sample_dish_data, sample_ingredient_data):
        """Test updating a dish."""
        # Create ingredient and dish
        client.post("/api/ingredients", json=sample_ingredient_data)
        client.post("/api/dishes/new", json=sample_dish_data)
        
        # Get dish ID
        response = client.get("/api/dishes")
        dish_id = response.json()[0]["id"]
        
        # Update dish
        update_data = {
            "ingredients": [{"name": "Test Ingredient", "amount": 200}]
        }
        response = client.post(f"/api/dishes/{dish_id}", json=update_data)
        assert response.status_code == 200
    
    def test_delete_dish(self, client: TestClient, sample_dish_data, sample_ingredient_data):
        """Test deleting a dish."""
        # Create ingredient and dish
        client.post("/api/ingredients", json=sample_ingredient_data)
        client.post("/api/dishes/new", json=sample_dish_data)
        
        # Get dish ID
        response = client.get("/api/dishes")
        dish_id = response.json()[0]["id"]
        
        # Delete dish
        response = client.delete(f"/api/dishes/{dish_id}")
        assert response.status_code == 200
        
        # Verify deletion
        response = client.get("/api/dishes")
        assert len(response.json()) == 0


class TestGoalsEndpoints:
    """Tests for nutrition goals."""
    
    def test_get_default_goals(self, client: TestClient):
        """Test getting default goals."""
        response = client.get("/api/goals")
        assert response.status_code == 200
        data = response.json()
        assert "protein" in data
        assert "fat" in data
        assert "carbohydrates" in data
        assert "calories" in data
    
    def test_set_goals(self, client: TestClient):
        """Test setting nutrition goals."""
        goals_data = {
            "protein": 150,
            "fat": 70,
            "carbohydrates": 200,
            "calories": 2500
        }
        response = client.post("/api/goals", json=goals_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["goals"]["protein"] == 150


class TestMenuEndpoints:
    """Tests for menu processing."""
    
    def test_process_empty_menu(self, client: TestClient):
        """Test processing empty menu."""
        response = client.post("/api/menu", json={"dishes": []})
        assert response.status_code == 200
        data = response.json()
        assert data["dishes"] == []
        assert data["ingredients"] == {}
    
    def test_process_menu_with_dishes(
        self, 
        client: TestClient, 
        sample_dish_data, 
        sample_ingredient_data
    ):
        """Test processing menu with dishes."""
        # Create ingredient and dish
        client.post("/api/ingredients", json=sample_ingredient_data)
        client.post("/api/dishes/new", json=sample_dish_data)
        
        # Get dish ID
        response = client.get("/api/dishes")
        dish_id = response.json()[0]["id"]
        
        # Process menu
        menu_data = {"dishes": [{"id": dish_id, "portions": 2}]}
        response = client.post("/api/menu", json=menu_data)
        assert response.status_code == 200
        data = response.json()
        assert len(data["dishes"]) == 1
        assert "ingredients" in data
        assert "total_nutrition" in data


class TestPagination:
    """Tests for pagination functionality."""
    
    def test_ingredients_pagination(self, client: TestClient):
        """Test ingredients pagination."""
        # Create multiple ingredients
        for i in range(5):
            client.post("/api/ingredients", json={
                "name": f"Ingredient {i}",
                "nutrition": {"calories": 100, "proteins": 10, "fats": 5, "carbohydrates": 15}
            })
        
        # Test pagination
        response = client.get("/api/ingredients?skip=2&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
    
    def test_dishes_pagination(self, client: TestClient):
        """Test dishes pagination."""
        # Create ingredient first
        client.post("/api/ingredients", json={
            "name": "Common Ingredient",
            "nutrition": {"calories": 100, "proteins": 10, "fats": 5, "carbohydrates": 15}
        })
        
        # Create multiple dishes
        for i in range(5):
            client.post("/api/dishes/new", json={
                "name": f"Dish {i}",
                "ingredients": [{"name": "Common Ingredient", "amount": 100}]
            })
        
        # Test pagination
        response = client.get("/api/dishes?skip=2&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 2


class TestErrorHandling:
    """Tests for error handling."""
    
    def test_invalid_json(self, client: TestClient):
        """Test handling of invalid JSON."""
        response = client.post(
            "/api/ingredients",
            content="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422
    
    def test_missing_required_fields(self, client: TestClient):
        """Test handling of missing required fields."""
        response = client.post("/api/ingredients", json={"name": "Incomplete"})
        assert response.status_code == 422
    
    def test_negative_values(self, client: TestClient):
        """Test handling of negative values."""
        response = client.post("/api/ingredients", json={
            "name": "Invalid",
            "nutrition": {"calories": -100, "proteins": -10, "fats": -5, "carbohydrates": -15}
        })
        assert response.status_code == 422
