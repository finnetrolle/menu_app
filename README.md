# Menu Management System

This is a modern menu management application with nutritional calculation capabilities, built with a layered architecture following SOLID and KISS principles.

## Project Structure

```
menu_app/
├── app.py                          # Main application entry point
├── migrate_data.py                 # Data migration script
├── requirements.txt                # Python dependencies
├── .gitignore
├── LICENSE
├── README.md
├── docs/                           # Project documentation
│   ├── api_communication.md        # API documentation
│   ├── architecture.md             # Architectural decisions
│   ├── class_structure.md          # Class relationships
│   ├── kiss_principles.md          # KISS implementation
│   ├── project_structure.md        # Directory structure
│   └── solid_principles.md         # SOLID implementation
├── src/                            # Application source code
│   ├── database.py                 # Database connection and setup
│   ├── models/                     # Domain models
│   │   ├── __init__.py
│   │   ├── dish.py
│   │   ├── dish_loader.py
│   │   ├── ingredient.py
│   │   ├── ingredient_data_loader.py
│   │   ├── interfaces.py
│   │   ├── nutrition.py
│   │   └── nutrition_calculator.py
│   └── services/                   # Business logic
│       ├── dish_service.py
│       └── ingredient_service.py
├── static/                         # Static assets
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── add_dish.js
│       ├── app.js
│       └── edit_dish.js
├── templates/                      # HTML templates
│   ├── add_dish.html
│   ├── edit_dish.html
│   └── index.html
└── tests/                          # Test suite
    ├── conftest.py
    ├── test_api_endpoints.py
    ├── test_classes.py
    ├── test_data_loading.py
    ├── test_dish_loader.py
    ├── test_nutrition_basic.py
    └── test_nutrition_info.py
```

## Features

- **Dish Management**: Create, read, update and delete dishes
- **Nutritional Calculation**: Automatic calculation of total nutrients
- **Ingredient Management**: Comprehensive ingredient database
- **Responsive UI**: Mobile-friendly interface for all devices
- **RESTful API**: Well-documented endpoints for all functionality
- **Data Persistence**: Database-backed storage for all entities

## Setup Instructions

### Prerequisites
- Python 3.8+

### Installation
1. Create virtual environment (if not exists):
   ```bash
   python -m venv .venv
   ```
2. Activate virtual environment:
   - macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application
1. Ensure virtual environment is activated
2. Start the server:
   ```bash
   python app.py
   ```
3. The application will be available at `http://localhost:8000`

## API Endpoints

### Dish Management
- `GET /api/dishes` - Get all available dishes
- `GET /api/dishes/{id}` - Get detailed information about a dish
- `POST /api/dishes` - Create a new dish
- `PUT /api/dishes/{id}` - Update an existing dish
- `DELETE /api/dishes/{id}` - Delete a dish

### Ingredient Management
- `GET /api/ingredients` - Get all available ingredients
- `POST /api/ingredients` - Create a new ingredient
- `PUT /api/ingredients/{id}` - Update an ingredient
- `DELETE /api/ingredients/{id}` - Delete an ingredient

### Menu Calculation
- `POST /api/menu/calculate` - Calculate nutrients for selected dishes
  ```json
  {
    "dishes": [
      {"id": 1, "quantity": 2},
      {"id": 2, "quantity": 1}
    ]
  }
  ```

### Goal Management
- `POST /api/goals` - Set nutrient goals
  ```json
  {
    "protein_g": 150,
    "fat_g": 70,
    "carbohydrate_g": 200,
    "energy_kcal": 2500
  }
  ```
- `GET /api/goals` - Get current nutrient goals

## Architecture Overview

### Layered Architecture
- **Presentation Layer**: HTML templates and JavaScript
- **API Layer**: `app.py` handles HTTP requests
- **Service Layer**: Business logic in `src/services/`
- **Domain Model Layer**: Core entities in `src/models/`
- **Data Access Layer**: Database operations in `src/database.py` and loaders

### Key Design Principles
- **SOLID**: Applied throughout the codebase
- **KISS**: Simple solutions for complex problems
- **Separation of Concerns**: Clear boundaries between components
- **Testability**: Designed for easy unit and integration testing

## Data Management

### Database Structure
- **Ingredients table**: Stores ingredient definitions and nutritional values
- **Dishes table**: Stores dish metadata
- **Dish ingredients table**: Junction table for dish composition

### Data Flow
1. Application startup initializes database connection
2. Data loaders handle schema initialization and data population
3. Services interact with data layer through well-defined interfaces
4. All data operations are transaction-safe

## Development

### Backend Structure
- **Models**: `src/models/` - Domain entities and value objects
- **Services**: `src/services/` - Business logic implementation
- **Data Access**: `src/database.py` and loaders - Database operations

### Frontend Structure
- **Templates**: `templates/` - HTML templates
- **CSS**: `static/css/` - Stylesheets
- **JavaScript**: `static/js/` - Client-side functionality

## Testing

### Test Coverage
- **Models**: 95%+ coverage
- **Services**: 85%+ coverage
- **API endpoints**: 80%+ coverage

### Running Tests
To execute the full test suite:
```bash
pytest tests/
```

## Deployment

The application can be deployed to any platform that supports Python applications:
- Cloud platforms (AWS, GCP, Azure)
- Containerized deployment with Docker
- Traditional server environments

## Troubleshooting

### Database Initialization
If you encounter database errors:
```bash
# Run data migration script
python migrate_data.py
```

### Common Issues
- Ensure all dependencies are installed (`pip install -r requirements.txt`)
- Verify database connection settings
- Check that the application has write permissions for database files

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/AmazingFeature`
3. Commit your changes: `git commit -m 'Add some AmazingFeature'`
4. Push to the branch: `git push origin feature/AmazingFeature`
5. Open a pull request
