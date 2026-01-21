import csv
import json
import os
import re
from src.database import get_session, Ingredient, Dish, DishIngredient

def parse_amount(amount) -> float:
    """Конвертирует значение количества в число, обрабатывая строки и числа"""
    if isinstance(amount, (int, float)):
        return float(amount)
    if isinstance(amount, str):
        match = re.search(r'[\d.]+', amount)
        if match:
            return float(match.group())
    return 0.0
def migrate_ingredients(session):
    """Миграция данных об ингредиентах из CSV в БД"""
    with open('data/ingredients.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row['name'].strip().lower()
            # Проверяем существование ингредиента (регистронезависимо)
            if not session.query(Ingredient).filter(Ingredient.name.ilike(name)).first():
                ingredient = Ingredient(
                    name=name,
                    protein_g=float(row['protein_g']),
                    fat_g=float(row['fat_g']),
                    carbohydrates_g=float(row['carbohydrates_g'])
                )
                session.add(ingredient)
    session.commit()

def migrate_dishes(session):
    """Миграция блюд из JSON-файлов в БД"""
    for filename in os.listdir('dishes'):
        if filename.endswith('.json'):
            with open(f'dishes/{filename}', 'r', encoding='utf-8') as f:
                dish_data = json.load(f)
                # Создаем блюдо
                dish = Dish(name=dish_data['name'].strip())
                session.add(dish)
                session.flush()  # Получаем dish.id до коммита
                
                # Обрабатываем ингредиенты
                for ing_data in dish_data.get('ingredients', []):
                    ing_name = ing_data['name'].strip().lower()
                    amount = parse_amount(ing_data['amount'])
                    
                    # Находим ингредиент по имени
                    ingredient = session.query(Ingredient).filter(Ingredient.name.ilike(ing_name)).first()
                    if ingredient:
                        dish_ing = DishIngredient(
                            dish_id=dish.id,
                            ingredient_id=ingredient.id,
                            amount=amount
                        )
                        session.add(dish_ing)
    session.commit()

if __name__ == '__main__':
    session = get_session()
    try:
        migrate_ingredients(session)
        migrate_dishes(session)
        print("Миграция данных успешно завершена!")
    finally:
        session.close()
