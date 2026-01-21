from sanic import Sanic, response
from sanic.response import html, json, file
import os
import csv
import json as json_module
import glob

from src.models import Ingredient, Dish, NutritionInfo, NutritionCalculator, IngredientDataLoader, DishLoader
from src.models.interfaces import IngredientLoaderInterface, DishLoaderInterface, NutritionCalculatorInterface

app = Sanic("menu_app")


# Хранилище данных о блюдах
dishes = []
nutrient_goals = {
    "protein": 0,
    "fat": 0,
    "carbohydrates": 0,
    "calories": 0
}

# Инициализация данных при запуске
ingredients_loader = IngredientDataLoader()
ingredients = ingredients_loader.load_ingredients()
dishes_loader = DishLoader()
raw_dishes = dishes_loader.load_dishes(ingredient_dict=ingredients)

# Инициализируем калькулятор питания
nutrition_calculator = NutritionCalculator()

# Функция для обновления данных блюд
def update_dishes_data():
    global dishes
    dishes = []
    for i, dish in enumerate(raw_dishes):
        # Calculate total nutrition for this dish using the ingredients and their amounts
        # Create a list of ingredients with their weights to pass to the calculator
        # Calculate total nutrition for this dish using the nutrition calculator
        ingredients_nutrition = {name: ingredient.nutrition for name, ingredient in ingredients.items()}
        total_nutrition = nutrition_calculator.calculate_total_nutrition_info(
            ingredients_nutrition=ingredients_nutrition,
            dish_ingredients=dish.ingredients
        )
        
        # For compatibility with frontend, convert to dictionary format
        dishes.append({
            "id": i + 1,
            "name": dish.name,
            "weight_g": round(dish.total_weight, 2),
            "energy_kcal": round(total_nutrition.calories, 2),
            "protein_g": round(total_nutrition.proteins, 2),
            "carbohydrates_g": round(total_nutrition.carbohydrates, 2),
            "fat_g": round(total_nutrition.fats, 2),
        })

# Инициализируем данные блюд
update_dishes_data()

# API endpoint для получения списка ингредиентов
@app.route("/api/ingredients", methods=["GET"])
async def get_ingredients(request):
    ingredients_list = []
    for idx, (name, ingredient) in enumerate(ingredients.items(), 1):
        ingredients_list.append({
            "id": idx,
            "name": name,
            "nutrition": {
                "calories": ingredient.nutrition.calories,
                "proteins": ingredient.nutrition.proteins,
                "fats": ingredient.nutrition.fats,
                "carbohydrates": ingredient.nutrition.carbohydrates
            }
        })
    return json(ingredients_list)

# Добавление нового ингредиента
@app.route("/api/ingredients", methods=["POST"])
async def add_ingredient(request):
    global ingredients
    data = request.json
    name = data.get("name")
    nutrition_data = data.get("nutrition", {})
    
    if not name or not nutrition_data:
        return json({"error": "Invalid data"}, status=400)
    
    # Создаем объект NutritionInfo
    nutrition = NutritionInfo(
        calories=nutrition_data.get("calories", 0),
        proteins=nutrition_data.get("proteins", 0),
        fats=nutrition_data.get("fats", 0),
        carbohydrates=nutrition_data.get("carbohydrates", 0)
    )
    
    # Создаем и добавляем ингредиент в глобальный словарь
    new_ingredient = Ingredient(name=name, nutrition=nutrition)
    ingredients[name] = new_ingredient
    
    # Сохраняем обновленный словарь напрямую
    ingredients_loader.save(ingredients)
    
    return json({"status": "success"})

# Обновление существующего ингредиента
@app.route("/api/ingredients/<name:str>", methods=["PUT"])
async def update_ingredient(request, name):
    global ingredients
    if name not in ingredients:
        return json({"error": "Ingredient not found"}, status=404)
    
    data = request.json
    nutrition_data = data.get("nutrition", {})
    
    if not nutrition_data:
        return json({"error": "Invalid data"}, status=400)
    
    # Создаем обновленный объект NutritionInfo
    nutrition = NutritionInfo(
        calories=nutrition_data.get("calories", 0),
        proteins=nutrition_data.get("proteins", 0),
        fats=nutrition_data.get("fats", 0),
        carbohydrates=nutrition_data.get("carbohydrates", 0)
    )
    
    # Обновляем ингредиент в глобальном словаре
    updated_ingredient = Ingredient(name=name, nutrition=nutrition)
    ingredients[name] = updated_ingredient
    
    # Сохраняем обновленный словарь напрямую
    ingredients_loader.save(ingredients)
    
    return json({"status": "success"})

# Удаление ингредиента
@app.route("/api/ingredients/<name:str>", methods=["DELETE"])
async def delete_ingredient(request, name):
    global ingredients
    if name not in ingredients:
        return json({"error": "Ingredient not found"}, status=404)
    
    # Удаляем ингредиент из глобального словаря
    del ingredients[name]
    
    # Сохраняем обновленный словарь напрямую
    ingredients_loader.save(ingredients)
    
    return json({"status": "success"})

# Calculate actual nutritional values for each dish and prepare data for frontend
# Using the nutrition calculator to handle calculations
nutrition_calculator = NutritionCalculator()
dishes = []
for i, dish in enumerate(raw_dishes):
    # Calculate total nutrition for this dish using the ingredients and their amounts
    # Create a list of ingredients with their weights to pass to the calculator
    # Calculate total nutrition for this dish using the nutrition calculator
    ingredients_nutrition = {name: ingredient.nutrition for name, ingredient in ingredients.items()}
    total_nutrition = nutrition_calculator.calculate_total_nutrition_info(
        ingredients_nutrition=ingredients_nutrition,
        dish_ingredients=dish.ingredients
    )
    
    # For compatibility with frontend, convert to dictionary format
    dishes.append({
        "id": i + 1,
        "name": dish.name,
        "weight_g": round(dish.total_weight, 2),
        "energy_kcal": round(total_nutrition.calories, 2),
        "protein_g": round(total_nutrition.proteins, 2),
        "carbohydrates_g": round(total_nutrition.carbohydrates, 2),
        "fat_g": round(total_nutrition.fats, 2),
    })

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
    return json(dishes)

@app.route("/api/goals", methods=["POST"])
async def set_goals(request):
    print("I'm in MAIN APP")
    global nutrient_goals
    data = request.json
    nutrient_goals = {
        "protein": float(data.get("protein", 0)),
        "fat": float(data.get("fat", 0)),
        "carbohydrates": float(data.get("carbohydrates", 0)),
        "calories": float(data.get("calories", 0))
    }
    return json({"status": "success", "goals": nutrient_goals})

@app.route("/api/goals", methods=["GET"])
async def get_goals(request):
    return json(nutrient_goals)

@app.route("/api/menu", methods=["POST"])
async def process_menu(request):
    data = request.json
    selected_dishes = data.get("dishes", [])
    
    # Сбор продуктов с суммированием весов для одинаковых ингредиентов
    ingredients = {}
    
    for dish in selected_dishes:
        dish_obj = next((d for d in dishes if d["id"] == dish["id"]), None)
        if not dish_obj:
            continue
            
        portions = dish.get("portions", 1)
        
        # Находим соответствующий объект Dish по имени
        dish_name = dish_obj["name"]
        real_dish = None
        for d in raw_dishes:
            if d.name == dish_name:
                real_dish = d
                break
        
        if real_dish:
            # Проходим по ингредиентам блюда и суммируем их веса
            for ingredient_name, weight in real_dish.ingredients.items():
                # Умножаем на количество порций
                total_weight = weight * portions
                
                if ingredient_name not in ingredients:
                    ingredients[ingredient_name] = {
                        "amount": 0,
                        "unit": "г"
                    }
                ingredients[ingredient_name]["amount"] += total_weight
    
    # Сортируем ингредиенты по алфавиту
    sorted_ingredients = dict(sorted(ingredients.items()))
    
    # Подсчет общего состава (по необходимости)
    total_nutrients = {
        "protein": 0,
        "fat": 0,
        "carbohydrates": 0,
        "calories": 0
    }
    
    # Суммируем питательные значения для всех ингредиентов
    for ingredient_name, weight_info in sorted_ingredients.items():
        if ingredient_name in ingredients:
            # Получаем информацию о питательных веществах из словаря ингредиентов
            ingredient = ingredients[ingredient_name]
            # Для примера, предположим, что в словаре ингредиентов есть данные о питательности
            # Или можно использовать реальные данные из данных ингредиентов, если они доступны
            # Но пока не будем пересчитывать общую питательность, так как задача только про ингредиенты
    
    return json({
        "total_nutrients": total_nutrients,
        "ingredients": sorted_ingredients
    })

@app.route("/api/dish/<dish_id:int>", methods=["GET"])
async def get_dish_ingredients(request, dish_id):
    if dish_id <= 0 or dish_id > len(raw_dishes):
        return json({"error": "Invalid dish ID"}, status=404)
    
    dish = raw_dishes[dish_id - 1]
    
    # Формируем список ингредиентов с рассчитанным КБЖУ для указанного веса
    ingredients_list = []
    for name, amount in dish.ingredients.items():
        if name in ingredients:
            ingredient_obj = ingredients[name]
            nutrition = ingredient_obj.nutrition
            
            # Рассчитываем КБЖУ для указанного веса ингредиента в блюде
            scaled_calories = nutrition.calories * amount / 100
            scaled_proteins = nutrition.proteins * amount / 100
            scaled_fats = nutrition.fats * amount / 100
            scaled_carbohydrates = nutrition.carbohydrates * amount / 100
            
            ingredients_list.append({
                "name": name,
                "amount": amount,
                "unit": "г",
                "calories": round(scaled_calories, 2),
                "proteins": round(scaled_proteins, 2),
                "fats": round(scaled_fats, 2),
                "carbohydrates": round(scaled_carbohydrates, 2)
            })
        else:
            # Если ингредиент не найден в базе, добавляем без КБЖУ
            ingredients_list.append({
                "name": name,
                "amount": amount,
                "unit": "г"
            })
    
    return json({
        "id": dish_id,
        "name": dish.name,
        "ingredients": ingredients_list
    })

@app.route("/edit_dish/<dish_id:int>")
async def edit_dish_page(request, dish_id):
    if dish_id <= 0 or dish_id > len(raw_dishes):
        return json({"error": "Invalid dish ID"}, status=404)
    with open("templates/edit_dish.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return html(html_content)

@app.route("/add_dish")
async def add_dish_page(request):
    with open("templates/add_dish.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return html(html_content)

@app.route("/api/dish/<dish_id:int>", methods=["POST"])
async def update_dish(request, dish_id):
    if dish_id <= 0 or dish_id > len(raw_dishes):
        return json({"error": "Invalid dish ID"}, status=404)
    
    data = request.json
    new_ingredients = data.get("ingredients", [])
    
    dish = raw_dishes[dish_id - 1]
    
    # Обновляем веса ингредиентов
    # Полностью заменяем ингредиенты, чтобы учесть новые добавленные
    dish.ingredients = {ing["name"]: ing["amount"] for ing in new_ingredients}
    
    # Сохраняем обновленное блюдо
    dish_data = {
        "name": dish.name,
        "ingredients": dish.ingredients
    }
    dishes_loader.save(dish_data)
    update_dishes_data()
    
    return json({"status": "success"})

@app.route("/api/dish/new", methods=["POST"])
async def create_dish(request):
    data = request.json
    dish_name = data.get("name")
    ingredients = data.get("ingredients", [])
    
    if not dish_name:
        return json({"error": "Dish name is required"}, status=400)
    
    # Создаем новое блюдо
    new_dish = {
        "name": dish_name,
        "ingredients": {ing["name"]: ing["amount"] for ing in ingredients}
    }
    
    # Сохраняем новое блюдо
    dishes_loader.save(new_dish)
    
    # Перезагружаем данные блюд
    global raw_dishes
    raw_dishes = dishes_loader.load_dishes(ingredient_dict=ingredients)
    
    # Обновляем данные блюд
    update_dishes_data()
    
    return json({"status": "success"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
