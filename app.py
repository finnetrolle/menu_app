from sanic import Sanic, response
from sanic.response import html, json, file
import os
import csv
import json as json_module
import glob

from src.models import Ingredient, Dish, NutritionInfo, NutritionCalculator, IngredientDataLoader, DishLoader
from src.models.interfaces import IngredientLoaderInterface, DishLoaderInterface, NutritionCalculatorInterface
from src.services.dish_service import DishService
from src.services.ingredient_service import IngredientService

app = Sanic("menu_app")

# Инициализация сервисов
ingredients_loader = IngredientDataLoader()
dishes_loader = DishLoader()
nutrition_calculator = NutritionCalculator()

ingredient_service = IngredientService(ingredients_loader)
dish_service = DishService(dishes_loader, ingredients_loader, nutrition_calculator)

# API endpoint для получения списка ингредиентов
@app.route("/api/ingredients", methods=["GET"])
async def get_ingredients(request):
    return json(ingredient_service.get_ingredients())

# Добавление нового ингредиента
@app.route("/api/ingredients", methods=["POST"])
async def add_ingredient(request):
    try:
        data = request.json
        name = data.get("name")
        nutrition_data = data.get("nutrition", {})
        ingredient_service.add_ingredient(name, nutrition_data)
        return json({"status": "success"})
    except ValueError as e:
        return json({"error": str(e)}, status=400)

# Обновление существующего ингредиента
@app.route("/api/ingredients/<id:int>", methods=["PUT"])
async def update_ingredient(request, id):
    try:
        # Получаем имя ингредиента по ID
        ingredients_list = ingredient_service.get_ingredients()
        target = next((item for item in ingredients_list if item["id"] == id), None)
        if not target:
            return json({"error": "Ingredient not found"}, status=404)
        
        name = target["name"]
        data = request.json
        nutrition_data = data.get("nutrition", {})
        
        ingredient_service.update_ingredient(name, nutrition_data)
        return json({"status": "success"})
    except ValueError as e:
        return json({"error": str(e)}, status=400)

# Удаление ингредиента
@app.route("/api/ingredients/<id:int>", methods=["DELETE"])
async def delete_ingredient(request, id):
    try:
        # Получаем имя ингредиента по ID
        ingredients_list = ingredient_service.get_ingredients()
        target = next((item for item in ingredients_list if item["id"] == id), None)
        if not target:
            return json({"error": "Ingredient not found"}, status=404)
        
        name = target["name"]
        ingredient_service.delete_ingredient(name)
        return json({"status": "success"})
    except ValueError as e:
        return json({"error": str(e)}, status=400)

# Удалено - логика перенесена в DishService

@app.route("/")
async def index(request):
    # Читаем HTML файл напрямую, без дублирования
    with open("templates/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return html(html_content)

# Обработка статических файлов
@app.route("/static/<path:path>")
async def static_files(request, path):
    try:
        return await file(f"static/{path}")
    except Exception:
        return response.text("File not found", status=404)

@app.route("/api/dishes", methods=["GET"])
async def get_dishes(request):
    return json(dish_service.get_dishes())

class GoalService:
    """Сервис для управления целевыми значениями питания"""
    def __init__(self):
        self.goals = {
            "protein": 0,
            "fat": 0,
            "carbohydrates": 0,
            "calories": 0
        }
    
    def set_goals(self, data: dict):
        """Установка целевых значений"""
        self.goals = {
            "protein": float(data.get("protein", 0)),
            "fat": float(data.get("fat", 0)),
            "carbohydrates": float(data.get("carbohydrates", 0)),
            "calories": float(data.get("calories", 0))
        }
        return self.goals
    
    def get_goals(self):
        """Получение текущих целевых значений"""
        return self.goals

# Инициализация сервиса целей
goal_service = GoalService()

@app.route("/api/goals", methods=["POST"])
async def set_goals(request):
    data = request.json
    goals = goal_service.set_goals(data)
    return json({"status": "success", "goals": goals})

@app.route("/api/goals", methods=["GET"])
async def get_goals(request):
    return json(goal_service.get_goals())

@app.route("/api/menu", methods=["POST"])
async def process_menu(request):
    data = request.json
    selected_dishes = data.get("dishes", [])
    result = dish_service.process_menu(selected_dishes)
    return json(result)

@app.route("/api/dish/<dish_id:int>", methods=["GET"])
async def get_dish_ingredients(request, dish_id):
    try:
        return json(dish_service.get_dish_ingredients(dish_id))
    except ValueError as e:
        return json({"error": str(e)}, status=404)

@app.route("/edit_dish/<dish_id:int>")
async def edit_dish_page(request, dish_id):
    try:
        # Проверяем существование блюда через сервис
        dish_service.get_dish_ingredients(dish_id)
        with open("templates/edit_dish.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        return html(html_content)
    except ValueError:
        return json({"error": "Invalid dish ID"}, status=404)

@app.route("/add_dish")
async def add_dish_page(request):
    with open("templates/add_dish.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return html(html_content)

@app.route("/api/dish/<dish_id:int>", methods=["POST"])
async def update_dish(request, dish_id):
    try:
        data = request.json
        new_ingredients = data.get("ingredients", [])
        dish_service.update_dish(dish_id, new_ingredients)
        return json({"status": "success"})
    except ValueError as e:
        return json({"error": str(e)}, status=400)

@app.route("/api/dish/new", methods=["POST"])
async def create_dish(request):
    try:
        data = request.json
        dish_name = data.get("name")
        ingredients = data.get("ingredients", [])
        
        if not dish_name:
            return json({"error": "Dish name is required"}, status=400)
        
        dish_service.create_dish(dish_name, ingredients)
        return json({"status": "success"})
    except ValueError as e:
        return json({"error": str(e)}, status=400)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
