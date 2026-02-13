"""
Pytest configuration and fixtures.
Provides test database setup and common fixtures.
"""

import pytest
import tempfile
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from src.database import Base, get_db
from src.api.main import app


# Test database setup
@pytest.fixture(scope="function")
def test_db():
    """Create a fresh test database for each test."""
    # Create temporary database file
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    database_url = f"sqlite:///{db_path}"
    
    # Create engine and tables
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    
    # Create session factory
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    yield TestingSessionLocal
    
    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture(scope="function")
def db_session(test_db):
    """Get a database session for testing."""
    session = test_db()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client(test_db):
    """Create a test client with database override."""
    def override_get_db():
        try:
            db = test_db()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def sample_ingredient_data():
    """Sample ingredient data for testing."""
    return {
        "name": "Test Ingredient",
        "nutrition": {
            "calories": 100,
            "proteins": 10,
            "fats": 5,
            "carbohydrates": 15
        }
    }


@pytest.fixture
def sample_dish_data():
    """Sample dish data for testing."""
    return {
        "name": "Test Dish",
        "ingredients": [
            {"name": "Test Ingredient", "amount": 100}
        ]
    }


@pytest.fixture
def create_test_ingredient(client, sample_ingredient_data):
    """Helper fixture to create a test ingredient."""
    response = client.post("/api/ingredients", json=sample_ingredient_data)
    return response.json()


@pytest.fixture
def create_test_dish(client, sample_dish_data, create_test_ingredient):
    """Helper fixture to create a test dish with ingredient."""
    response = client.post("/api/dishes/new", json=sample_dish_data)
    return response.json()
