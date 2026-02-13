# Menu Management System

Современное веб-приложение для управления меню с расчётом пищевой ценности блюд.

## Технологический стек

| Компонент | Технология |
|-----------|------------|
| Frontend | React 19 + TypeScript + Vite + Tailwind CSS |
| Backend | FastAPI + Pydantic + SQLAlchemy 2.0 |
| Database | SQLite (разработка) / PostgreSQL (production) |
| Infrastructure | Docker + Docker Compose + Alembic |

## Быстрый старт

### Development (локальная разработка)

**Терминал 1 - Backend:**
```bash
source .venv/bin/activate  # macOS/Linux
# или
.venv\Scripts\activate     # Windows

uvicorn src.api.main:app --reload --port 8000
```

**Терминал 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

Приложение будет доступно:
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

### Production (Docker)

```bash
docker-compose up --build
```

Приложение будет доступно:
- Frontend: `http://localhost`
- Backend API: `http://localhost:8000/api`
- API Docs: `http://localhost:8000/docs`

## Структура проекта

```
menu_app/
├── frontend/                    # React Frontend
│   ├── src/
│   │   ├── components/          # UI компоненты
│   │   ├── pages/               # Страницы
│   │   ├── hooks/               # TanStack Query хуки
│   │   ├── services/            # API клиент
│   │   └── types/               # TypeScript типы
│   ├── Dockerfile
│   └── nginx.conf
│
├── src/                         # Python Backend
│   ├── api/
│   │   ├── main.py              # FastAPI приложение
│   │   ├── config.py            # Конфигурация
│   │   ├── routes/              # API маршруты
│   │   └── schemas/             # Pydantic модели
│   ├── models/                  # Доменные модели
│   ├── services/                # Бизнес-логика
│   └── database.py              # SQLAlchemy модели
│
├── alembic/                     # Миграции БД
├── tests/                       # Тесты
├── docker-compose.yml
├── Dockerfile.backend
├── requirements.txt
└── pytest.ini
```

## API Endpoints

### Блюда
| Method | Path | Описание |
|--------|------|----------|
| GET | `/api/dishes` | Список всех блюд |
| GET | `/api/dishes/{id}` | Детали блюда |
| POST | `/api/dishes/new` | Создать блюдо |
| POST | `/api/dishes/{id}` | Обновить блюдо |
| DELETE | `/api/dishes/{id}` | Удалить блюдо |

### Ингредиенты
| Method | Path | Описание |
|--------|------|----------|
| GET | `/api/ingredients` | Список ингредиентов |
| POST | `/api/ingredients` | Создать ингредиент |
| PUT | `/api/ingredients/{id}` | Обновить ингредиент |
| DELETE | `/api/ingredients/{id}` | Удалить ингредиент |

### Прочее
| Method | Path | Описание |
|--------|------|----------|
| GET/POST | `/api/goals` | Цели питания |
| POST | `/api/menu` | Расчёт меню |
| GET | `/health` | Health check |

## Разработка

### Установка зависимостей

**Backend:**
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### Запуск тестов

```bash
source .venv/bin/activate
PYTHONPATH=. pytest tests/ -v
```

### Миграции базы данных

```bash
# Создать миграцию
alembic revision --autogenerate -m "Description"

# Применить миграции
alembic upgrade head

# Откатить миграцию
alembic downgrade -1
```

### Линтинг и форматирование

**Backend:**
```bash
# Форматирование не требуется (Python)
```

**Frontend:**
```bash
cd frontend
npm run lint
npm run lint:fix
npm run format
```

## Переменные окружения

Создайте файл `.env` в корне проекта:

```env
# Database
DATABASE_URL=sqlite:///./menu.db

# API
API_PREFIX=/api
DEBUG=true

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost
```

## Docker

### Сборка и запуск

```bash
# Сборка и запуск
docker-compose up --build

# Фоновый режим
docker-compose up -d

# Остановка
docker-compose down

# Просмотр логов
docker-compose logs -f
```

### Отдельные контейнеры

```bash
# Только backend
docker build -f Dockerfile.backend -t menu-backend .
docker run -p 8000:8000 menu-backend

# Только frontend
cd frontend
docker build -t menu-frontend .
docker run -p 80:80 menu-frontend
```

## Лицензия

MIT License - см. файл [LICENSE](LICENSE)
