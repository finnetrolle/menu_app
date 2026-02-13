"""
API endpoint tests for FastAPI application.
Uses httpx for async HTTP testing.
"""
import pytest
from httpx import AsyncClient, ASGITransport
from src.api.main import app


@pytest.fixture
async def client():
    """Create async test client for FastAPI app."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_get_ingredients(client: AsyncClient):
    """Test getting all ingredients."""
    response = await client.get("/api/ingredients")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_create_ingredient(client: AsyncClient):
    """Test creating a new ingredient."""
    data = {
        "name": "Test Ingredient",
        "nutrition": {
            "calories": 100,
            "proteins": 10,
            "fats": 5,
            "carbohydrates": 15
        }
    }
    response = await client.post("/api/ingredients", json=data)
    assert response.status_code == 200
    assert response.json()["status"] == "success"


@pytest.mark.asyncio
async def test_update_ingredient(client: AsyncClient):
    """Test updating an ingredient."""
    # First create a test ingredient
    create_data = {
        "name": "Ingredient To Update",
        "nutrition": {"calories": 100, "proteins": 5, "fats": 2, "carbohydrates": 10}
    }
    await client.post("/api/ingredients", json=create_data)
    
    # Get the ingredient ID
    list_response = await client.get("/api/ingredients")
    ingredients = list_response.json()
    ingredient_id = next(
        (ing["id"] for ing in ingredients if ing["name"] == "Ingredient To Update"),
        None
    )
    
    if ingredient_id:
        # Update the ingredient
        update_data = {
            "calories": 200,
            "proteins": 10,
            "fats": 4,
            "carbohydrates": 20
        }
        response = await client.put(f"/api/ingredients/{ingredient_id}", json=update_data)
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_ingredient(client: AsyncClient):
    """Test deleting an ingredient."""
    # First create a test ingredient
    create_data = {
        "name": "Ingredient To Delete",
        "nutrition": {"calories": 50, "proteins": 2, "fats": 1, "carbohydrates": 5}
    }
    await client.post("/api/ingredients", json=create_data)
    
    # Get the ingredient ID
    list_response = await client.get("/api/ingredients")
    ingredients = list_response.json()
    ingredient_id = next(
        (ing["id"] for ing in ingredients if ing["name"] == "Ingredient To Delete"),
        None
    )
    
    if ingredient_id:
        response = await client.delete(f"/api/ingredients/{ingredient_id}")
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_dishes(client: AsyncClient):
    """Test getting all dishes."""
    response = await client.get("/api/dishes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_set_and_get_goals(client: AsyncClient):
    """Test setting and getting nutrition goals."""
    # Set goals
    goals_data = {
        "protein": 150,
        "fat": 70,
        "carbohydrates": 200,
        "calories": 2500
    }
    set_response = await client.post("/api/goals", json=goals_data)
    assert set_response.status_code == 200
    
    # Get goals
    get_response = await client.get("/api/goals")
    assert get_response.status_code == 200
    goals = get_response.json()
    assert goals["protein"] == 150


@pytest.mark.asyncio
async def test_process_menu(client: AsyncClient):
    """Test processing menu."""
    menu_data = {
        "dishes": []
    }
    response = await client.post("/api/menu", json=menu_data)
    assert response.status_code == 200
    assert "ingredients" in response.json()


@pytest.mark.asyncio
async def test_get_dish_ingredients(client: AsyncClient):
    """Test getting dish ingredients."""
    # First get dishes to find an ID
    dishes_response = await client.get("/api/dishes")
    dishes = dishes_response.json()
    
    if dishes:
        dish_id = dishes[0]["id"]
        response = await client.get(f"/api/dishes/{dish_id}")
        assert response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_create_dish(client: AsyncClient):
    """Test creating a new dish."""
    dish_data = {
        "name": "Test Dish",
        "ingredients": []
    }
    response = await client.post("/api/dishes/new", json=dish_data)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """Test health check endpoint."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_root_endpoint(client: AsyncClient):
    """Test root endpoint."""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "docs" in data
