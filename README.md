# Menu Planning Application

This is a modern, refactored version of a menu planning application with nutritional calculation capabilities.

## Project Structure

```
menu_app/
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── data/
│   └── ingredients.csv
├── dishes/
│   ├── банан.json
│   ├── бигус.json
│   ├── борщ.json
│   ├── винегрет.json
│   ├── глазунья.json
│   ├── греча с молоком.json
│   ├── картофель фри.json
│   ├── китайский салат.json
│   ├── кофе с молоком.json
│   ├── куриное филе.json
│   ├── минтай.json
│   ├── овсяная каша.json
│   ├── окрошка.json
│   ├── оливье.json
│   ├── омлет.json
│   ├── паста барилла 100.json
│   ├── стакан кефира.json
│   ├── чашушули.json
│   ├── шин рамен.json
│   ├── щи.json
│   └── яблоко.json
├── docs/
│   ├── architecture.md
│   ├── class_structure.md
│   ├── fowler_refactorings.md
│   ├── kiss_principles.md
│   ├── project_structure.md
│   └── solid_principles.md
├── old_data/
│   └── foods.csv
├── src/
│   └── models/
│       ├── __init__.py
│       ├── dish_loader.py
│       ├── dish.py
│       ├── ingredient_data_loader.py
│       ├── ingredient.py
│       ├── interfaces.py
│       ├── nutrition_calculator.py
│       └── nutrition.py
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── app.js
│       └── edit_dish.js
├── templates/
│   ├── edit_dish.html
│   └── index.html
└── tests/
    ├── test_classes.py
    ├── test_data_loading.py
    ├── test_dish_loader.py
    ├── test_nutrition_basic.py
    └── test_nutrition_info.py
```
## Features

- **Dish Management**: View and select from available dishes
- **Nutritional Calculation**: Calculate total nutrients for selected menu items
- **Ingredient Tracking**: Track ingredients used in the menu
- **Responsive UI**: Modern, mobile-friendly interface
- **API Integration**: RESTful API endpoints for all functionality


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
1. Ensure virtual environment is activated (see Installation section)
2. Start the server:
   ```bash
   python app.py
   ```

3. The application will be available at `http://127.0.0.1:8000`

## API Endpoints

### Dishes
- `GET /api/dishes` - Get all available dishes
- `GET /api/dishes/{id}` - Get a specific dish by ID

### Menu
- `POST /api/menu` - Calculate nutrients for selected dishes
- `POST /api/menu/ingredients` - Get ingredients list for menu

### Goals
- `POST /api/goals` - Set nutrient goals
- `GET /api/goals` - Get current nutrient goals

## Architecture Overview

### Backend
- Built with Sanic (Python web framework)
- Modular architecture with separate models, services, and API layers
- RESTful API design
- Error handling and validation

### Frontend
- Built with React (JavaScript)
- Component-based architecture
- Responsive design
- State management for selected dishes and calculations

## Data Management

### Ingredients Database
The application uses a CSV file to store ingredient data:

```
name,energy_kcal,protein_g,carbohydrates_g,fat_g
Омлет,150,12,3,10
Овсянка,350,12,60,8
Салат Цезарь,250,15,10,20
Куриная грудка,165,31,0,3.6
Рис,130,2.7,28.5,0.3
Брокколи,34,2.8,7,0.4
Яйца,155,13,1.1,11
Творог 5% жирности,83,12,4.6,2.7
Молоко 2.5% жирности,42,3.4,4.8,2.5
Картофель,86,2,19,0.1
Банан,89,1.1,22.8,0.3
Яблоко,52,0.3,13.8,0.2
Апельсин,47,0.9,11.8,0.1
```

### Dish Definitions
Each dish is defined in a separate JSON file:

```json
{
  "name": "Омлет",
  "ingredients": [
    {
      "name": "Яйца",
      "amount": 60
    },
    {
      "name": "Молоко 2.5% жирности",
      "amount": 20
    },
    {
      "name": "Сливочное масло",
      "amount": 2
    }
  ]
}
```

## Development

### Backend Development
- All backend code is in `src/backend/`
- Models are in `models/` directory
- Services are in `services/` directory  
- API endpoints are in `api/` directory

### Frontend Development
- All frontend code is in `src/frontend/`
- Components are in `components/` directory
- Entry point is `index.js`
- Styling is in `App.css`


## Testing

### Backend Tests
- Unit tests for models and services
- Integration tests for API endpoints
- Test coverage for nutrient calculation logic

## Running Tests
To execute the test suite:
```bash
pytest tests/
```

## Deployment

The application can be deployed to any platform that supports Python and Node.js applications:
- Cloud platforms (AWS, GCP, Azure)
- Containerized deployment with Docker
- Serverless platforms

## Troubleshooting

### Python Import Errors
If you encounter import errors related to `distutils`, try:
```bash
# On macOS with Python 3.13, you might need to install the distutils package
# This is a known issue with Python 3.13 and some packages
pip install setuptools
```

### Frontend Build Issues
If the frontend build fails:
1. Ensure Node.js is properly installed
2. Run `npm install` to install all dependencies
3. Check that the React version is compatible with the project

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/AmazingFeature`
3. Commit your changes: `git commit -m 'Add some AmazingFeature'`
4. Push to the branch: `git push origin feature/AmazingFeature`
5. Open a pull request
