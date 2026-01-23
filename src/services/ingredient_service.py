from typing import Dict, List
from src.models import Ingredient, NutritionInfo
from src.models.ingredient_data_loader import IngredientDataLoader
from src.models.interfaces import IngredientLoaderInterface

class IngredientService:
    """
    Сервисный слой для управления ингредиентами.
    Инкапсулирует бизнес-логику и валидацию данных.
    """
    
    def __init__(self, ingredient_loader: IngredientLoaderInterface):
        """
        Инициализация сервиса с DAO.
        
        Args:
            ingredient_loader: DAO для работы с ингредиентами
        """
        self.ingredient_loader = ingredient_loader
        self._refresh_data()
    
    def _refresh_data(self):
        """Перезагрузка данных из хранилища"""
        self.ingredients = self.ingredient_loader.load_ingredients()
    
    def get_ingredients(self) -> List[Dict]:
        """
        Получение списка ингредиентов в формате API.
        
        Returns:
            List[Dict]: Список ингредиентов с ID и питанием
        """
        ingredients_list = []
        for idx, (name, ingredient) in enumerate(self.ingredients.items(), 1):
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
        return ingredients_list
    
    def _validate_nutrition(self, nutrition_data: Dict) -> NutritionInfo:
        """
        Валидация и преобразование данных питания.
        
        Args:
            nutrition_data: Сырые данные о питании
            
        Returns:
            NutritionInfo: Валидированный объект
            
        Raises:
            ValueError: При невалидных данных
        """
        try:
            return NutritionInfo(
                calories=float(nutrition_data.get("calories", 0)),
                proteins=float(nutrition_data.get("proteins", 0)),
                fats=float(nutrition_data.get("fats", 0)),
                carbohydrates=float(nutrition_data.get("carbohydrates", 0))
            )
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid nutrition data: {str(e)}")
    
    def add_ingredient(self, name: str, nutrition_data: Dict):
        """
        Добавление нового ингредиента с валидацией.
        
        Args:
            name: Название ингредиента
            nutrition_data: Данные о питании
            
        Raises:
            ValueError: При невалидных данных
        """
        if not name or not nutrition_data:
            raise ValueError("Name and nutrition data are required")
        
        nutrition = self._validate_nutrition(nutrition_data)
        new_ingredient = Ingredient(name=name, nutrition=nutrition)
        self.ingredients[name] = new_ingredient
        self.ingredient_loader.save(self.ingredients)
        self._refresh_data()
    
    def update_ingredient(self, name: str, nutrition_data: Dict):
        """
        Обновление существующего ингредиента.
        
        Args:
            name: Название ингредиента
            nutrition_data: Новые данные о питании
            
        Raises:
            ValueError: При невалидных данных или отсутствии ингредиента
        """
        if name not in self.ingredients:
            raise ValueError("Ingredient not found")
        
        nutrition = self._validate_nutrition(nutrition_data)
        updated_ingredient = Ingredient(name=name, nutrition=nutrition)
        self.ingredients[name] = updated_ingredient
        self.ingredient_loader.save(self.ingredients)
        self._refresh_data()
    
    def delete_ingredient(self, name: str):
        """
        Удаление ингредиента.
        
        Args:
            name: Название ингредиента
            
        Raises:
            ValueError: При отсутствии ингредиента
        """
        if name not in self.ingredients:
            raise ValueError("Ingredient not found")
        
        del self.ingredients[name]
        self.ingredient_loader.save(self.ingredients)
        self._refresh_data()
