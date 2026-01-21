# Рефакторинг согласно рекомендациям Мартина Фаулера

Этот документ описывает реализацию рекомендаций Мартина Фаулера в процессе рефакторинга приложения.

## Extract Interface
- Создан интерфейс `IngredientLoaderInterface` в `src/models/interfaces.py`
- Создан интерфейс `DishLoaderInterface` в `src/models/interfaces.py`  
- Создан интерфейс `NutritionCalculatorInterface` в `src/models/interfaces.py`

## Replace Magic Number with Symbolic Constant
- В `app.py` заменены магические числа в расчетах на переменные с понятными именами
- Использованы стандартные значения питательных веществ (4 ккал/г для белков и углеводов, 9 ккал/г для жиров)

## Inline Temporary Variable
- В `app.py` упрощена логика расчета питательной ценности блюд
- Удалены временные переменные, которые можно было сразу использовать

## Extract Method
- Логика расчета питательной ценности вынесена в отдельный метод `calculate_total_nutrition_info`
- Логика загрузки данных вынесена в отдельные методы `load_ingredients` и `load_dishes`

## Replace Conditional with Polymorphism
- Вместо условных конструкций для обработки разных типов данных используется полиморфизм через интерфейсы
- Классы `IngredientDataLoader`, `DishLoader` и `NutritionCalculator` реализуют свои интерфейсы

## Move Method
- Методы расчета питательной ценности перенесены из классов `Dish` в `NutritionCalculator`
- Методы загрузки данных перенесены из классов в отдельные сервисы

## Extract Class
- Создан класс `interfaces.py` для хранения всех интерфейсов приложения
- Это упрощает понимание зависимостей между компонентами

## Replace Inheritance with Delegation
- Компоненты больше не зависят напрямую от конкретных классов, а работают через интерфейсы
- Это делает систему более гибкой и легко расширяемой

## Introduce Parameter Object
- В методах `NutritionInfo.from_protein_fat_carb` и `NutritionCalculator.calculate_total_nutrition_info` 
  используются объекты с понятными именами параметров вместо списка аргументов

## Hide Delegate
- В `app.py` классы используются через интерфейсы, а не напрямую
- Это скрывает внутреннюю реализацию компонентов от основной логики приложения

## Replace Constructor with Factory Method
- Использованы методы фабрики через интерфейсы для создания объектов
- Это позволяет легче заменять реализации в будущем

## Extract Variable
- В `app.py` переменные с понятными именами вынесены из сложных выражений:
  - `ingredients_loader = IngredientDataLoader()`
  - `dishes_loader = DishLoader("dishes")`  
  - `nutrition_calculator = NutritionCalculator()`

## Remove Dead Code
- Удален ненужный код из `app.py`:
  - Старая логика расчета питательной ценности вручную
  - Неиспользуемый импорт `json_module` и `glob`
