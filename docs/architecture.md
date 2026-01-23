# System Architecture

## Overview
This document describes the current layered architecture of the menu management application, showing component interactions and data flow.

## Component Diagram

```
┌─────────────┐       ┌─────────────┐       ┌───────────────────┐       ┌───────────────────┐
│   Browser   │──────▶│   API Layer │──────▶│   Service Layer   │──────▶│   Data Layer      │
│ (Frontend)  │◀──────│ (app.py)    │◀──────│ (services/)       │◀──────│ (models/, database)│
└─────────────┘       └─────────────┘       └───────────────────┘       └───────────────────┘
```

## Layered Architecture

### 1. Presentation Layer (Frontend)
- **Components**: HTML templates, CSS, JavaScript
- **Location**: `templates/`, `static/`
- **Responsibilities**:
  - User interface rendering
  - Form handling for dish management
  - API communication via JavaScript
  - Dynamic content updates

### 2. API Layer
- **Component**: `app.py`
- **Responsibilities**:
  - HTTP request handling
  - Route definition and validation
  - Request/response serialization
  - Error handling
  - Authentication (if implemented)

### 3. Service Layer
- **Components**: `src/services/`
  - `dish_service.py`
  - `ingredient_service.py`
- **Responsibilities**:
  - Business logic implementation
  - Data validation
  - Transaction management
  - Service composition
  - Error handling specific to business rules

### 4. Domain Model Layer
- **Components**: `src/models/`
  - `dish.py`, `ingredient.py`
  - `nutrition.py`, `nutrition_calculator.py`
  - `interfaces.py`
- **Responsibilities**:
  - Core business entities
  - Value objects
  - Domain services
  - Business rules enforcement

### 5. Data Access Layer
- **Components**:
  - `src/database.py`
  - `src/models/ingredient_data_loader.py`
  - `src/models/dish_loader.py`
- **Responsibilities**:
  - Database connection management
  - Data persistence
  - Data retrieval
  - Data transformation between storage and domain models

## Data Flow

### Dish Management Flow
1. Frontend makes GET request to `/api/dishes`
2. API layer routes to appropriate handler in `app.py`
3. `DishService.get_all_dishes()` is called
4. Service layer retrieves data from database via `DishLoader`
5. Domain models are converted to API response format
6. Response is sent back to frontend

### Dish Creation Flow
1. Frontend makes POST request to `/api/dishes` with dish data
2. API layer validates request format
3. `DishService.create_dish()` processes the request
4. Service validates business rules (e.g., ingredient availability)
5. `NutritionCalculator` computes total nutrition values
6. Data is persisted via `database.py`
7. Created dish is returned to frontend

### Menu Calculation Flow
1. Frontend makes POST request to `/api/menu/calculate` with dish IDs
2. `DishService.calculate_menu_nutrition()` processes the request
3. Service retrieves dishes and their ingredients
4. `NutritionCalculator` aggregates values across all dishes
5. Response with total nutrition and per-dish breakdown is generated
6. Response is returned to frontend

## Data Persistence

### Database Structure
- **Ingredients table**: Stores ingredient definitions and nutritional values
- **Dishes table**: Stores dish metadata
- **Dish ingredients table**: Junction table for dish composition

### Data Loading Process
1. Application startup initializes database connection
2. Data loaders (`ingredient_data_loader.py`, `dish_loader.py`) handle:
   - Schema initialization
   - Data migration (if needed)
   - Initial data population

## Testing Strategy

### Test Layers
- **Unit tests**: `tests/test_*.py` - Isolated component testing
- **Integration tests**: `tests/test_api_endpoints.py` - API and service layer
- **End-to-end tests**: (Not currently implemented)

### Test Coverage
- Models: 95%+
- Services: 85%+
- API endpoints: 80%+

## Key Architectural Decisions

1. **Separation of Concerns**:
   - Clear boundaries between layers
   - Each component has single responsibility
   - Easy to modify or replace individual layers

2. **Domain-Driven Design**:
   - Business logic encapsulated in domain models
   - Services orchestrate domain objects
   - Rich model semantics

3. **Testability**:
   - Dependency injection for test doubles
   - Isolated unit tests
   - Clear test boundaries

4. **Scalability**:
   - Stateless API layer
   - Database abstraction
   - Modular service components
