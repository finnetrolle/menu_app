# Menu App - Документация проекта

## Обзор проекта

Веб-приложение для управления меню и расчета пищевой ценности блюд.

### Технологический стек

| Компонент | Технология |
|-----------|------------|
| Backend | FastAPI + SQLAlchemy 2.0 |
| Database | SQLite + Alembic (миграции) |
| Frontend | React 18 + TypeScript + Vite |
| Styling | Tailwind CSS |
| State Management | TanStack Query |
| Containerization | Docker + Docker Compose |

---

## Архитектура

### Структура проекта

```
menu_app/
├── src/                          # Backend
│   ├── api/                      # API слой
│   │   ├── main.py               # Точка входа FastAPI
│   │   ├── config.py             # Конфигурация
│   │   ├── routes/               # API маршруты
│   │   │   ├── dishes.py
│   │   │   ├── ingredients.py
│   │   │   ├── goals.py
│   │   │   └── menu.py
│   │   └── schemas/              # Pydantic схемы
│   ├── models/                   # Доменные модели
│   │   ├── dish.py
│   │   ├── ingredient.py
│   │   ├── nutrition.py
│   │   └── nutrition_calculator.py
│   ├── services/                 # Бизнес-логика
│   │   ├── dish_service.py
│   │   └── ingredient_service.py
│   └── database.py               # Работа с БД
├── frontend/                     # Frontend
│   ├── src/
│   │   ├── components/           # React компоненты
│   │   ├── pages/                # Страницы
│   │   ├── hooks/                # Кастомные хуки
│   │   ├── services/             # API клиент
│   │   └── types/                # TypeScript типы
│   └── ...
├── alembic/                      # Миграции БД
├── tests/                        # Тесты
└── docs/                         # Документация
```

### Слоистая архитектура

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    Frontend     │────▶│    API Layer    │────▶│  Service Layer  │
│  (React + TS)   │◀────│   (FastAPI)     │◀────│   (services/)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                                                        ▼
                                                ┌─────────────────┐
                                                │   Data Layer    │
                                                │ (models/, db)   │
                                                └─────────────────┘
```

---

## API Документация

### Управление ингредиентами

#### Получение списка ингредиентов
```
GET /api/ingredients
```
**Ответ:**
```json
[
  {
    "id": 1,
    "name": "Курица",
    "calories": 165,
    "protein_g": 31,
    "fat_g": 3.6,
    "carbohydrate_g": 0
  }
]
```

#### Добавление ингредиента
```
POST /api/ingredients
```
**Тело запроса:**
```json
{
  "name": "Новый ингредиент",
  "calories": 100,
  "protein_g": 10,
  "fat_g": 5,
  "carbohydrate_g": 20
}
```

#### Обновление ингредиента
```
PUT /api/ingredients/{id}
```

#### Удаление ингредиента
```
DELETE /api/ingredients/{id}
```

### Управление блюдами

#### Получение списка блюд
```
GET /api/dishes
```
**Ответ:**
```json
[
  {
    "id": 1,
    "name": "Салат Цезарь",
    "total_weight_g": 250.0,
    "energy_kcal": 320.5,
    "protein_g": 18.2,
    "carbohydrate_g": 12.7,
    "fat_g": 22.3
  }
]
```

#### Получение деталей блюда
```
GET /api/dishes/{id}
```
**Ответ:**
```json
{
  "id": 1,
  "name": "Салат Цезарь",
  "total_weight_g": 250.0,
  "energy_kcal": 320.5,
  "protein_g": 18.2,
  "carbohydrate_g": 12.7,
  "fat_g": 22.3,
  "ingredients": [
    {
      "name": "Курица",
      "amount_g": 100,
      "calories": 165,
      "protein_g": 31,
      "fat_g": 3.6,
      "carbohydrate_g": 0
    }
  ]
}
```

#### Создание блюда
```
POST /api/dishes
```
**Тело запроса:**
```json
{
  "name": "Новое блюдо",
  "ingredients": [
    {"name": "Ингредиент1", "amount_g": 100},
    {"name": "Ингредиент2", "amount_g": 50}
  ]
}
```

#### Обновление блюда
```
PUT /api/dishes/{id}
```

#### Удаление блюда
```
DELETE /api/dishes/{id}
```

### Управление целями питания

#### Установка целей
```
POST /api/goals
```
**Тело запроса:**
```json
{
  "protein_g": 150,
  "fat_g": 70,
  "carbohydrate_g": 200,
  "energy_kcal": 2500
}
```

#### Получение текущих целей
```
GET /api/goals
```

### Расчет меню

#### Расчет питательной ценности меню
```
POST /api/menu/calculate
```
**Тело запроса:**
```json
{
  "dishes": [
    {"id": 1, "quantity": 2},
    {"id": 2, "quantity": 1}
  ]
}
```
**Ответ:**
```json
{
  "total_energy_kcal": 850.5,
  "total_protein_g": 45.2,
  "total_carbohydrate_g": 32.7,
  "total_fat_g": 52.3,
  "dishes": [...]
}
```

---

## Модели данных

### Nutrition (Питательная ценность)
```python
class Nutrition:
    energy_kcal: float      # Калории (ккал)
    protein_g: float        # Белки (г)
    fat_g: float            # Жиры (г)
    carbohydrate_g: float   # Углеводы (г)
```

### Ingredient (Ингредиент)
```python
class Ingredient:
    id: int                 # Уникальный идентификатор
    name: str               # Название ингредиента
    nutrition: Nutrition    # Питательная ценность на 100г
```

### Dish (Блюдо)
```python
class Dish:
    id: int                 # Уникальный идентификатор
    name: str               # Название блюда
    ingredients: List[Dict] # Список ингредиентов с количеством
```

---

## Принципы разработки

### KISS (Keep It Simple, Stupid)
- Четкое разделение на слои с минимальной связностью
- Каждый компонент имеет единственную ответственность
- Использование простых структур данных

### SOLID
- **Single Responsibility**: Каждый класс решает одну задачу
- **Open/Closed**: Расширение через интерфейсы без изменения кода
- **Liskov Substitution**: Взаимозаменяемость реализаций интерфейсов
- **Interface Segregation**: Узкоспециализированные интерфейсы
- **Dependency Inversion**: Зависимость от абстракций, не реализаций

---

## Запуск проекта

### Разработка (локально)

**Backend:**
```bash
pip install -r requirements.txt
alembic upgrade head
uvicorn src.api.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Docker

```bash
docker-compose up --build
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## Тестирование

```bash
# Запуск всех тестов
pytest

# С покрытием
pytest --cov=src tests/
```

### Структура тестов
- `test_api_endpoints.py` - Тесты API
- `test_classes.py` - Тесты моделей
- `test_nutrition_*.py` - Тесты расчетов питательной ценности
- `test_dish_loader.py` - Тесты загрузки данных
