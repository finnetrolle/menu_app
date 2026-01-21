# Class Structure Implementation

This document describes the implemented class structure for the nutrition tracking system.

## Classes

### NutritionInfo
Contains nutritional information (КБЖУ) for ingredients or dishes.

**Attributes:**
- calories (float): Energy content in kilocalories
- fats (float): Fat content in grams  
- proteins (float): Protein content in grams
- carbohydrates (float): Carbohydrate content in grams

**Usage:**
```python
nutrition = NutritionInfo(
    calories=100.0,
    fats=5.0,
    proteins=10.0,
    carbohydrates=20.0
)
```

### Ingredient
Represents an ingredient with its name and nutritional information.

**Attributes:**
- name (str): Name of the ingredient
- nutrition (NutritionInfo): Nutritional information for the ingredient (calculated per 100g)

**Usage:**
```python
ingredient = Ingredient(
    name="Молоко",
    nutrition=NutritionInfo(
        calories=42.0,
        fats=3.5,
        proteins=3.4,
        carbohydrates=4.8
    )
)
```

### Dish
Represents a dish with its ingredients and methods to calculate nutritional information.

**Attributes:**
- name (str): Name of the dish
- ingredients (Dict[str, float]): Dictionary mapping ingredient names to their weights in grams

**Methods:**
- get_total_nutrition_info(ingredient_list: list) -> NutritionInfo:
  Calculates total nutritional information for the dish based on ingredients and their weights
- get_total_weight() -> float:
  Calculates the total weight of the dish in grams

**Usage:**
```python
dish = Dish(
    name="Омлет",
    ingredients={
        "Молоко": 100.0,
        "Яйца": 150.0
    }
)

# Calculate total nutrition for the dish
total_nutrition = dish.get_total_nutrition_info([milk_ingredient, egg_ingredient])
total_weight = dish.get_total_weight()
```

## Implementation Details

The Dish class was enhanced to:
1. Store ingredient names and their weights in grams
2. Calculate total nutritional information by converting per-100g values to actual amounts based on ingredient weights
3. Calculate the total weight of the dish in grams

This implementation follows the requirement that КБЖУ values are calculated for 100g as specified on product packaging.
