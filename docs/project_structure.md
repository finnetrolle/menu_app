# Структура проекта menu_app

## Общая структура

```
menu_app/
├── app.py                          # Основной файл приложения (backend)
├── migrate_data.py                 # Скрипт миграции данных
├── requirements.txt                # Зависимости Python
├── .gitignore
├── LICENSE
├── README.md
├── docs/                           # Документация проекта
│   ├── api_communication.md        # Документация API
│   ├── architecture.md             # Архитектурные решения
│   ├── class_structure.md          # Структура классов
│   ├── kiss_principles.md          # Принципы KISS
│   ├── project_structure.md        # Текущая документация
│   └── solid_principles.md         # Принципы SOLID
├── src/                            # Источники приложения
│   ├── database.py                 # Работа с базой данных
│   ├── models/                     # Модели данных
│   │   ├── __init__.py
│   │   ├── dish.py
│   │   ├── dish_loader.py
│   │   ├── ingredient.py
│   │   ├── ingredient_data_loader.py
│   │   ├── interfaces.py
│   │   ├── nutrition.py
│   │   └── nutrition_calculator.py
│   └── services/                   # Бизнес-логика
│       ├── dish_service.py
│       └── ingredient_service.py
├── static/                         # Статические файлы
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── add_dish.js
│       ├── app.js
│       └── edit_dish.js
├── templates/                      # HTML шаблоны
│   ├── add_dish.html
│   ├── edit_dish.html
│   └── index.html
└── tests/                          # Тесты
    ├── conftest.py
    ├── test_api_endpoints.py
    ├── test_classes.py
    ├── test_data_loading.py
    ├── test_dish_loader.py
    ├── test_nutrition_basic.py
    └── test_nutrition_info.py
```

## Подробное описание структуры

### 1. app.py
- Основной файл Python приложения
- Инициализирует веб-сервер и подключает маршруты
- Использует Sanic framework для обработки HTTP-запросов

### 2. src/
- **database.py**: Реализация работы с базой данных
- **models/**: Содержит классы для представления данных
  - **dish.py**: Модель блюда
  - **ingredient.py**: Модель ингредиента
  - **nutrition_calculator.py**: Логика расчета питательной ценности
  - **dish_loader.py** и **ingredient_data_loader.py**: Загрузчики данных
- **services/**: Бизнес-логика приложения
  - **dish_service.py**: Сервис для работы с блюдами
  - **ingredient_service.py**: Сервис для работы с ингредиентами

### 3. static/
- **css/style.css**: Основные стили приложения
- **js/**: JavaScript для интерактивности
  - **app.js**: Основной скрипт приложения
  - **add_dish.js** и **edit_dish.js**: Скрипты для форм

### 4. templates/
- HTML-шаблоны для веб-интерфейса
- **index.html**: Главная страница
- **add_dish.html** и **edit_dish.html**: Формы добавления/редактирования

### 5. tests/
- Модульные тесты для всех компонентов
- **test_api_endpoints.py**: Тесты API
- **test_nutrition_*.py**: Тесты расчета питательной ценности
- **test_dish_loader.py**: Тесты загрузки данных о блюдах

### 6. migrate_data.py
- Скрипт для миграции данных между форматами

## Использование

### Запуск приложения
1. Установите зависимости: `pip install -r requirements.txt`
2. Запустите сервер: `python app.py`
3. Откройте в браузере: `http://localhost:8000`

### Тестирование
