# Class Structure Implementation

This document describes the implemented class structure for the menu management system.

## Core Models

### Nutrition
Represents nutritional information for ingredients or dishes.

**Attributes:**
- energy_kcal (float): Energy content in kilocalories
- protein_g (float): Protein content in grams
- fat_g (float): Fat content in grams
- carbohydrate_g (float): Carbohydrate content in grams

**Usage:**
```python
nutrition = Nutrition(
    energy_kcal=100.0,
    protein_g=10.0,
    fat_g=5.0,
    carbohydrate_g=20.0
)
```

### Ingredient
Represents a food ingredient with its nutritional profile.

**Attributes:**
- id (int): Unique identifier
- name (str): Name of the ingredient
- nutrition (Nutrition): Nutritional information per 100g

**Usage:**
```python
ingredient = Ingredient(
    id=1,
    name="Молоко",
    nutrition=Nutrition(
        energy_kcal=42.0,
        protein_g=3.4,
        fat_g=3.5,
        carbohydrate_g=4.8
    )
)
```

### Dish
Represents a prepared dish composed of multiple ingredients.

**Attributes:**
- id (int): Unique identifier
- name (str): Name of the dish
- ingredients (List[Dict]): List of ingredient components with amounts

**Structure of ingredients:**
```python
[
    {
        "ingredient_id": 1,
        "amount_g": 100.0,
        "ingredient": Ingredient  # Reference to Ingredient object
    }
]
```

**Methods:**
- calculate_nutrition() -> Nutrition:
  Calculates total nutritional value of the dish based on ingredients
- get_total_weight() -> float:
  Returns total weight of the dish in grams

**Usage:**
```python
dish = Dish(
    id=1,
    name="Омлет",
    ingredients=[
        {"ingredient_id": 1, "amount_g": 100.0},
        {"ingredient_id": 2, "amount_g": 150.0}
    ]
)

# Calculate total nutrition for the dish
total_nutrition = dish.calculate_nutrition()
total_weight = dish.get_total_weight()
```

## Service Layer

### NutritionCalculator
Utility class for nutritional calculations.

**Methods:**
- calculate_ingredient_nutrition(ingredient: Ingredient, amount_g: float) -> Nutrition:
  Calculates nutrition for specific amount of ingredient
- calculate_dish_nutrition(ingredients: List[Dict]) -> Nutrition:
  Aggregates nutrition values for all ingredients in a dish

### DishService
Business logic for dish management.

**Methods:**
- create_dish(name: str, ingredients: List[Dict]) -> Dish:
  Creates and validates new dish
- update_dish(dish_id: int, **kwargs) -> Dish:
  Updates existing dish
- get_dish_with_ingredients(dish_id: int) -> Dict:
  Returns dish with full ingredient details

### IngredientService
Business logic for ingredient management.

**Methods:**
- get_all_ingredients() -> List[Ingredient]:
  Returns all available ingredients
- create_ingredient(**kwargs) -> Ingredient:
  Creates new ingredient with validation
- update_ingredient(ingredient_id: int, **kwargs) -> Ingredient:
  Updates existing ingredient

## Implementation Details

The system follows these key patterns:

1. **Separation of concerns**:
   - Models (`src/models/`) contain data structures
   - Services (`src/services/`) contain business logic
   - Data loaders handle persistence

2. **Nutrition calculation**:
   - All calculations are based on per-100g values
   - Total values are proportional to ingredient amounts
   - Uses `NutritionCalculator` for consistent calculations

3. **Data flow**:
   - Frontend → API endpoints → Service layer → Models
   - Data loaders handle database interactions
   - Services validate and transform data
