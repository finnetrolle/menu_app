from typing import List, Dict
from src.models import Dish, NutritionInfo, NutritionCalculator
from src.models.dish_loader import DishLoader
from src.models.ingredient_data_loader import IngredientDataLoader
from src.models.interfaces import IngredientLoaderInterface

class DishService:
    """
    Сервисный слой для управления блюдами и их обработки.
    Реализует бизнес-логику, изолированную от контроллеров и DAO.
    """
    
    def __init__(
        self,
        dish_loader: DishLoader,
        ingredient_loader: IngredientLoaderInterface,
        nutrition_calculator: NutritionCalculator
    ):
        """
        Инициализация сервиса с зависимостями.
        
        Args:
            dish_loader: DAO для работы с блюдами
            ingredient_loader: DAO для работы с ингредиентами
            nutrition_calculator: Сервис для расчёта питания
        """
        self.dish_loader = dish_loader
        self.ingredient_loader = ingredient_loader
        self.nutrition_calculator = nutrition_calculator
        self._refresh_data()
    
    def _refresh_data(self):
        """Обновление внутренних данных после изменений"""
        self.ingredients = self.ingredient_loader.load_ingredients()
        self.raw_dishes = self.dish_loader.load_dishes(self.ingredients)
    
    def get_dishes(self) -> List[Dict]:
        """
        Получение списка блюд с расчётным питанием.
        
        Returns:
            List[Dict]: Список блюд с расчётными значениями КБЖУ
        """
        dishes = []
        for i, dish in enumerate(self.raw_dishes):
            ingredients_nutrition = {name: ing.nutrition for name, ing in self.ingredients.items()}
            total_nutrition = self.nutrition_calculator.calculate_total_nutrition_info(
                ingredients_nutrition=ingredients_nutrition,
                dish_ingredients=dish.ingredients
            )
            
            dishes.append({
                "id": i + 1,
                "name": dish.name,
                "weight_g": round(dish.total_weight, 2),
                "energy_kcal": round(total_nutrition.calories, 2),
                "protein_g": round(total_nutrition.proteins, 2),
                "carbohydrates_g": round(total_nutrition.carbohydrates, 2),
                "fat_g": round(total_nutrition.fats, 2),
            })
        return dishes
    
    def get_dish_ingredients(self, dish_id: int) -> Dict:
        """
        Получение ингредиентов конкретного блюда с расчётом КБЖУ.
        
        Args:
            dish_id: ID блюда
            
        Returns:
            Dict: Данные о блюде и его ингредиентах
            
        Raises:
            ValueError: При невалидном ID блюда
        """
        if dish_id <= 0 or dish_id > len(self.raw_dishes):
            raise ValueError("Invalid dish ID")
        
        dish = self.raw_dishes[dish_id - 1]
        ingredients_list = []
        
        for name, amount in dish.ingredients.items():
            if name in self.ingredients:
                ingredient_obj = self.ingredients[name]
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
        
        return {
            "id": dish_id,
            "name": dish.name,
            "ingredients": ingredients_list
        }
    
    def process_menu(self, selected_dishes: List[Dict]) -> Dict:
        """
        Обработка выбранного меню для расчёта ингредиентов.
        
        Args:
            selected_dishes: Список выбранных блюд с количеством порций
            
        Returns:
            Dict: Список ингредиентов с суммарными весами
        """
        ingredients = {}
        
        for dish in selected_dishes:
            dish_obj = next((d for d in self.raw_dishes if d.id == dish["id"]), None)
            if not dish_obj:
                continue
                
            portions = dish.get("portions", 1)
            
            for name, weight in dish_obj.ingredients.items():
                total_weight = weight * portions
                
                if name not in ingredients:
                    ingredients[name] = {"amount": 0, "unit": "г"}
                ingredients[name]["amount"] += total_weight
        
        return {"ingredients": dict(sorted(ingredients.items()))}
    
    def update_dish(self, dish_id: int, new_ingredients: List[Dict]):
        """
        Обновление состава блюда.
        
        Args:
            dish_id: ID блюда
            new_ingredients: Новый список ингредиентов
        """
        if dish_id <= 0 or dish_id > len(self.raw_dishes):
            raise ValueError("Invalid dish ID")
        
        dish = self.raw_dishes[dish_id - 1]
        dish_data = {
            "name": dish.name,
            "ingredients": {ing["name"]: ing["amount"] for ing in new_ingredients}
        }
        
        self.dish_loader.save(dish_data)
        self._refresh_data()
    
    def create_dish(self, name: str, ingredients: List[Dict]):
        """
        Создание нового блюда.
        
        Args:
            name: Название блюда
            ingredients: Список ингредиентов
        """
        dish_data = {
            "name": name,
            "ingredients": {ing["name"]: ing["amount"] for ing in ingredients}
        }
        
        self.dish_loader.save(dish_data)
        self._refresh_data()
