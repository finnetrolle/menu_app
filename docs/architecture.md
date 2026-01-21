# Architecture Diagram

## Overview
This document describes the architectural structure of the menu planning application, showing how components interact with each other.

```

## Component Interactions

### 1. Frontend-Backend Communication
```
┌─────────────┐           ┌─────────────┐
│   Browser   │───────────┤   Sanic     │
│             │           │   Server    │
│  React UI   │           │             │
│             │           │             │
└─────────────┘           └─────────────┘
```

### 2. Data Flow

#### Dish Loading:
1. Frontend makes GET request to `/api/dishes`
2. Backend reads all JSON files from `dishes/` directory
3. Backend loads ingredient data from `data/ingredients.csv`
4. Backend calculates nutrient values for each dish using ingredients
5. Backend returns list of dishes to frontend

#### Menu Generation:
1. Frontend makes POST request to `/api/menu` with selected dishes
2. Backend calculates total nutrients for selected dishes
3. Backend aggregates ingredients from all selected dishes
4. Backend returns calculated nutrients and ingredient list to frontend

#### Goal Setting:
1. Frontend makes POST request to `/api/goals` with goal values
2. Backend stores goals in memory
3. Backend returns confirmation to frontend

#### Goal Retrieval:
1. Frontend makes GET request to `/api/goals`
2. Backend returns current goal values from memory

## API Endpoints Overview

### Dish Management
- `GET /api/dishes` - Returns all available dishes with calculated nutrients

### Menu Calculation
- `POST /api/menu` - Takes selected dishes and returns:
  - Total nutrient values (protein, fat, carbs, calories)
  - List of ingredients with amounts

### Goal Management
- `POST /api/goals` - Sets nutrient goals for the user
- `GET /api/goals` - Returns current nutrient goals

## Data Flow Details

### Dish Data Processing
1. `app.py` loads all JSON files from `dishes/`
2. For each dish, it reads the ingredient list
3. It looks up each ingredient in `data/ingredients.csv`
4. It calculates the total nutrients for each dish by summing up the nutrient contributions from ingredients

### Menu Generation Process
1. Frontend sends selected dishes to `/api/menu`
2. Backend calculates:
   - Total protein, fat, carbs, and calories
   - Ingredient list with total amounts (grams)
3. Returns both calculated nutrients and ingredient list

### Data Persistence
- Goals are stored in memory (temporary storage)
- Dish and ingredient data is loaded from files on each application start
