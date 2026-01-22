import pytest
from app import app

def test_get_ingredients():
    """Проверка получения списка ингредиентов"""
    request, response = app.test_client.get('/api/ingredients')
    assert response.status == 200
    assert isinstance(response.json, list)
    if len(response.json) > 0:
        assert 'id' in response.json[0]
        assert 'name' in response.json[0]
        assert 'nutrition' in response.json[0]

def test_create_ingredient():
    """Проверка добавления нового ингредиента"""
    new_ingredient = {
        "name": "Тестовый ингредиент",
        "nutrition": {
            "calories": 150,
            "proteins": 10,
            "fats": 5,
            "carbohydrates": 20
        }
    }
    
    request, response = app.test_client.post(
        '/api/ingredients', 
        json=new_ingredient
    )
    assert response.status == 200
    
    # Проверяем, что ингредиент появился в списке
    request, response = app.test_client.get('/api/ingredients')
    assert any(ing['name'] == 'Тестовый ингредиент' for ing in response.json)

def test_update_ingredient():
    """Проверка обновления ингредиента по ID"""
    # Сначала создаем тестовый ингредиент
    app.test_client.post('/api/ingredients', json={
        "name": "Для обновления",
        "nutrition": {"calories": 100, "proteins": 5, "fats": 2, "carbohydrates": 10}
    })
    
    # Получаем ID ингредиента
    request, response = app.test_client.get('/api/ingredients')
    ingredient_id = next(
        ing['id'] for ing in response.json 
        if ing['name'] == 'Для обновления'
    )
    
    # Обновляем данные
    updated_data = {
        "nutrition": {
            "calories": 200,
            "proteins": 15,
            "fats": 8,
            "carbohydrates": 25
        }
    }
    
    request, response = app.test_client.put(
        f'/api/ingredients/{ingredient_id}',
        json=updated_data
    )
    assert response.status == 200
    
    # Проверяем обновленные данные
    request, response = app.test_client.get('/api/ingredients')
    ingredient = next(ing for ing in response.json if ing['id'] == ingredient_id)
    assert ingredient['nutrition']['calories'] == 200

def test_delete_ingredient():
    """Проверка удаления ингредиента по ID"""
    # Создаем тестовый ингредиент
    app.test_client.post('/api/ingredients', json={
        "name": "Для удаления",
        "nutrition": {"calories": 50, "proteins": 3, "fats": 1, "carbohydrates": 5}
    })
    
    # Получаем ID
    request, response = app.test_client.get('/api/ingredients')
    ingredient_id = next(
        ing['id'] for ing in response.json 
        if ing['name'] == 'Для удаления'
    )
    
    # Удаляем
    request, response = app.test_client.delete(f'/api/ingredients/{ingredient_id}')
    assert response.status == 200
    
    # Проверяем отсутствие в списке по имени (ID динамически пересчитывается)
    request, response = app.test_client.get('/api/ingredients')
    assert not any(ing['name'] == 'Для удаления' for ing in response.json)

def test_get_dishes():
    """Проверка получения списка блюд"""
    request, response = app.test_client.get('/api/dishes')
    assert response.status == 200
    assert isinstance(response.json, list)
    if len(response.json) > 0:
        assert 'id' in response.json[0]
        assert 'name' in response.json[0]
        assert 'energy_kcal' in response.json[0]

def test_set_and_get_goals():
    """Проверка установки и получения целей питания"""
    goals = {
        "protein": 150,
        "fat": 70,
        "carbohydrates": 200,
        "calories": 2500
    }
    
    # Устанавливаем цели
    request, response = app.test_client.post('/api/goals', json=goals)
    assert response.status == 200
    
    # Получаем цели
    request, response = app.test_client.get('/api/goals')
    assert response.status == 200
    assert response.json == goals

def test_process_menu():
    """Проверка расчета состава меню"""
    # Получаем список блюд
    request, response = app.test_client.get('/api/dishes')
    dishes = response.json
    
    if len(dishes) > 0:
        menu_data = {
            "dishes": [
                {"id": dishes[0]['id'], "portions": 2}
            ]
        }
        
        request, response = app.test_client.post('/api/menu', json=menu_data)
        assert response.status == 200
        assert 'ingredients' in response.json
        assert isinstance(response.json['ingredients'], dict)

def test_get_dish_ingredients():
    """Проверка получения состава блюда по ID"""
    # Получаем список блюд
    request, response = app.test_client.get('/api/dishes')
    dishes = response.json
    
    if len(dishes) > 0:
        dish_id = dishes[0]['id']
        
        # Запрашиваем состав блюда
        request, response = app.test_client.get(f'/api/dish/{dish_id}')
        assert response.status == 200
        assert 'id' in response.json
        assert 'name' in response.json
        assert 'ingredients' in response.json
        if len(response.json['ingredients']) > 0:
            assert 'name' in response.json['ingredients'][0]
            assert 'amount' in response.json['ingredients'][0]

def test_create_dish():
    """Проверка создания нового блюда"""
    # Создаем тестовый ингредиент
    app.test_client.post('/api/ingredients', json={
        "name": "Тестовый ингредиент для блюда",
        "nutrition": {"calories": 100, "proteins": 10, "fats": 5, "carbohydrates": 20}
    })
    
    new_dish = {
        "name": "Тестовое блюдо",
        "ingredients": [
            {"name": "Тестовый ингредиент для блюда", "amount": 150}
        ]
    }
    
    # Создаем блюдо
    request, response = app.test_client.post('/api/dish/new', json=new_dish)
    assert response.status == 200
    
    # Проверяем, что блюдо появилось в списке
    request, response = app.test_client.get('/api/dishes')
    assert any(dish['name'] == 'Тестовое блюдо' for dish in response.json)
