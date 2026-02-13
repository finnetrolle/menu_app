# План рефакторинга: Современное веб-приложение

## Анализ текущего состояния

### Технологический стек
| Компонент | Текущее решение | Проблемы |
|-----------|-----------------|----------|
| Backend | Sanic | Хорошо, но можно улучшить |
| Database | SQLite + SQLAlchemy | Приемлемо для MVP |
| Frontend | React 17 (CDN) | ❌ Нет сборки, медленная загрузка |
| Transpilation | Babel standalone | ❌ Компиляция в браузере |
| State Management | useState hooks | ❌ Монолитный компонент |
| Styling | Bootstrap 5 + CSS | ✅ Приемлемо |
| Build Tool | Нет | ❌ Нет оптимизации |

### Выявленные проблемы

#### Frontend (Критические)
1. **Монолитный компонент**: [`app.js`](static/js/app.js) ~80KB в одном файле
2. **Нет сборки**: React загружается с CDN, JSX компилируется в браузере
3. **Нет модульности**: Весь код в одном компоненте App
4. **Нет типизации**: Отсутствует TypeScript
5. **Нет линтинга**: Нет ESLint/Prettier
6. **Медленная загрузка**: Babel standalone замедляет запуск

#### Backend (Средние)
1. **Смешивание ответственности**: [`app.py`](app.py) содержит и маршруты, и сервис GoalService
2. **Нет валидации**: Нет Pydantic моделей для валидации запросов
3. **Нет миграций**: Нет Alembic для управления схемой БД
4. **Нет контейнеризации**: Нет Docker

#### Инфраструктура (Средние)
1. **Нет CI/CD**: Нет автоматических проверок
2. **Нет Docker**: Сложность развертывания
3. **Нет переменных окружения**: Конфигурация захардкожена

---

## Целевая архитектура

### Технологический стек (Целевой)

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND                                │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────────┐ │
│  │   React 18  │  │ TypeScript  │  │ Vite (Build Tool)    │ │
│  │   + Vite    │  │             │  │                      │ │
│  └─────────────┘  └─────────────┘  └──────────────────────┘ │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────────┐ │
│  │ TanStack    │  │ Tailwind    │  │ React Router v6      │ │
│  │ Query       │  │ CSS         │  │                      │ │
│  └─────────────┘  └─────────────┘  └──────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      BACKEND                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────────┐ │
│  │   FastAPI   │  │  Pydantic   │  │ SQLAlchemy 2.0       │ │
│  │             │  │             │  │ + Alembic            │ │
│  └─────────────┘  └─────────────┘  └──────────────────────┘ │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────────┐ │
│  │  Pytest     │  │  Docker     │  │ PostgreSQL           │ │
│  │  + Coverage │  │  Compose    │  │ (опционально)        │ │
│  └─────────────┘  └─────────────┘  └──────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## Фазы рефакторинга

### Фаза 1: Подготовка инфраструктуры (Приоритет: Высокий)

#### 1.1 Настройка сборки Frontend
```bash
# Создание Vite + React + TypeScript проекта
npm create vite@latest frontend -- --template react-ts
```

**Структура frontend:**
```
frontend/
├── src/
│   ├── components/         # Переиспользуемые компоненты
│   │   ├── DishCard.tsx
│   │   ├── IngredientTable.tsx
│   │   ├── NutritionProgress.tsx
│   │   └── ui/             # Базовые UI компоненты
│   ├── pages/              # Страницы
│   │   ├── HomePage.tsx
│   │   ├── DishesPage.tsx
│   │   ├── IngredientsPage.tsx
│   │   └── EditDishPage.tsx
│   ├── hooks/              # Кастомные хуки
│   │   ├── useDishes.ts
│   │   ├── useIngredients.ts
│   │   └── useNutrition.ts
│   ├── services/           # API клиенты
│   │   └── api.ts
│   ├── types/              # TypeScript типы
│   │   └── index.ts
│   ├── store/              # Состояние (TanStack Query)
│   └── App.tsx
├── package.json
├── vite.config.ts
└── tsconfig.json
```

#### 1.2 Docker контейнеризация
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/menu
    depends_on:
      - db
  
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
  
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: menu
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

#### 1.3 CI/CD Pipeline
```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest --cov=src tests/

  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: cd frontend && npm ci
      - run: cd frontend && npm run lint
      - run: cd frontend && npm run test
      - run: cd frontend && npm run build
```

---

### Фаза 2: Рефакторинг Backend (Приоритет: Высокий)

#### 2.1 Миграция на FastAPI

**Преимущества:**
- Автоматическая документация (OpenAPI/Swagger)
- Валидация данных через Pydantic
- Асинхронность из коробки
- Лучший developer experience

**Новая структура:**
```
src/
├── main.py                 # Точка входа FastAPI
├── config.py               # Конфигурация через pydantic-settings
├── api/
│   ├── __init__.py
│   ├── deps.py             # Зависимости (DI)
│   ├── routes/
│   │   ├── dishes.py
│   │   ├── ingredients.py
│   │   └── goals.py
│   └── schemas/
│       ├── dish.py
│       ├── ingredient.py
│       └── nutrition.py
├── services/               # Бизнес-логика (сохраняется)
├── models/                 # Доменные модели (сохраняется)
└── db/
    ├── database.py
    ├── models.py           # SQLAlchemy модели
    └── repositories/
        ├── dish_repo.py
        └── ingredient_repo.py
```

#### 2.2 Pydantic схемы для валидации

```python
# src/api/schemas/dish.py
from pydantic import BaseModel
from typing import List, Optional

class IngredientInDish(BaseModel):
    name: str
    amount: float
    unit: str = "г"

class DishCreate(BaseModel):
    name: str
    ingredients: List[IngredientInDish]

class DishResponse(BaseModel):
    id: int
    name: str
    weight_g: float
    energy_kcal: float
    protein_g: float
    carbohydrates_g: float
    fat_g: float

    class Config:
        from_attributes = True
```

#### 2.3 Репозиторий pattern

```python
# src/db/repositories/dish_repo.py
from typing import List, Optional
from sqlalchemy.orm import Session
from src.db.models import Dish, DishIngredient

class DishRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self) -> List[Dish]:
        return self.db.query(Dish).all()
    
    def get_by_id(self, dish_id: int) -> Optional[Dish]:
        return self.db.query(Dish).filter(Dish.id == dish_id).first()
    
    def create(self, dish: Dish) -> Dish:
        self.db.add(dish)
        self.db.commit()
        self.db.refresh(dish)
        return dish
    
    def delete(self, dish_id: int) -> bool:
        dish = self.get_by_id(dish_id)
        if dish:
            self.db.delete(dish)
            self.db.commit()
            return True
        return False
```

#### 2.4 Alembic миграции

```bash
# Инициализация
alembic init alembic

# Создание миграции
alembic revision --autogenerate -m "Initial migration"

# Применение миграций
alembic upgrade head
```

---

### Фаза 3: Рефакторинг Frontend (Приоритет: Высокий)

#### 3.1 Разбиение на компоненты

**Текущий монолит (~2000 строк) → Модульная структура:**

```typescript
// frontend/src/types/index.ts
export interface Nutrition {
  calories: number;
  proteins: number;
  fats: number;
  carbohydrates: number;
}

export interface Dish {
  id: number;
  name: string;
  weight_g: number;
  energy_kcal: number;
  protein_g: number;
  carbohydrates_g: number;
  fat_g: number;
}

export interface Ingredient {
  id: number;
  name: string;
  nutrition: Nutrition;
}
```

#### 3.2 TanStack Query для управления состоянием

```typescript
// frontend/src/hooks/useDishes.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { dishesApi } from '../services/api';

export function useDishes() {
  return useQuery({
    queryKey: ['dishes'],
    queryFn: dishesApi.getAll,
  });
}

export function useCreateDish() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: dishesApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['dishes'] });
    },
  });
}

export function useDeleteDish() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: dishesApi.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['dishes'] });
    },
  });
}
```

#### 3.3 API клиент с типизацией

```typescript
// frontend/src/services/api.ts
import type { Dish, Ingredient, Nutrition } from '../types';

const API_BASE = '/api';

async function fetchJson<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(url, options);
  if (!response.ok) {
    throw new Error(`API Error: ${response.statusText}`);
  }
  return response.json();
}

export const dishesApi = {
  getAll: () => fetchJson<Dish[]>(`${API_BASE}/dishes`),
  
  getById: (id: number) => fetchJson<Dish>(`${API_BASE}/dishes/${id}`),
  
  create: (data: Omit<Dish, 'id'>) => 
    fetchJson<Dish>(`${API_BASE}/dishes`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }),
  
  update: (id: number, data: Partial<Dish>) =>
    fetchJson<Dish>(`${API_BASE}/dishes/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }),
  
  delete: (id: number) =>
    fetchJson<void>(`${API_BASE}/dishes/${id}`, { method: 'DELETE' }),
};

export const ingredientsApi = {
  getAll: () => fetchJson<Ingredient[]>(`${API_BASE}/ingredients`),
  
  create: (data: Omit<Ingredient, 'id'>) =>
    fetchJson<Ingredient>(`${API_BASE}/ingredients`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    }),
};
```

#### 3.4 Компоненты страниц

```typescript
// frontend/src/pages/HomePage.tsx
import { useDishes } from '../hooks/useDishes';
import { DishCard } from '../components/DishCard';
import { LoadingSpinner } from '../components/ui/LoadingSpinner';

export function HomePage() {
  const { data: dishes, isLoading, error } = useDishes();

  if (isLoading) return <LoadingSpinner />;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {dishes?.map((dish) => (
        <DishCard key={dish.id} dish={dish} />
      ))}
    </div>
  );
}
```

#### 3.5 Tailwind CSS вместо кастомного CSS

```typescript
// frontend/src/components/DishCard.tsx
import type { Dish } from '../types';

interface DishCardProps {
  dish: Dish;
}

export function DishCard({ dish }: DishCardProps) {
  return (
    <div className="bg-white rounded-lg shadow-md p-4 hover:shadow-lg transition-shadow">
      <h3 className="text-lg font-semibold text-gray-800">{dish.name}</h3>
      <div className="mt-2 space-y-1 text-sm text-gray-600">
        <p>Вес: <span className="font-medium">{dish.weight_g}г</span></p>
        <p>Калории: <span className="font-medium">{dish.energy_kcal} ккал</span></p>
        <div className="flex gap-2">
          <span className="px-2 py-1 bg-blue-100 rounded">Б: {dish.protein_g}г</span>
          <span className="px-2 py-1 bg-yellow-100 rounded">Ж: {dish.fat_g}г</span>
          <span className="px-2 py-1 bg-green-100 rounded">У: {dish.carbohydrates_g}г</span>
        </div>
      </div>
    </div>
  );
}
```

---

### Фаза 4: Тестирование (Приоритет: Средний)

#### 4.1 Backend тесты

```python
# tests/test_api/test_dishes.py
import pytest
from httpx import AsyncClient
from src.main import app

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

async def test_get_dishes(client: AsyncClient):
    response = await client.get("/api/dishes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

async def test_create_dish(client: AsyncClient):
    dish_data = {
        "name": "Test Dish",
        "ingredients": [
            {"name": "Chicken", "amount": 100}
        ]
    }
    response = await client.post("/api/dishes", json=dish_data)
    assert response.status_code == 201
```

#### 4.2 Frontend тесты

```typescript
// frontend/src/components/__tests__/DishCard.test.tsx
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { DishCard } from '../DishCard';

describe('DishCard', () => {
  const mockDish = {
    id: 1,
    name: 'Test Dish',
    weight_g: 200,
    energy_kcal: 300,
    protein_g: 20,
    fat_g: 10,
    carbohydrates_g: 30,
  };

  it('renders dish name', () => {
    render(<DishCard dish={mockDish} />);
    expect(screen.getByText('Test Dish')).toBeInTheDocument();
  });

  it('displays nutrition info', () => {
    render(<DishCard dish={mockDish} />);
    expect(screen.getByText(/300 ккал/)).toBeInTheDocument();
  });
});
```

---

### Фаза 5: Дополнительные улучшения (Приоритет: Низкий)

#### 5.1 Аутентификация (опционально)
- JWT токены
- OAuth2 интеграция
- Роли и права доступа

#### 5.2 PWA (Progressive Web App)
- Service Worker
- Офлайн поддержка
- Push уведомления

#### 5.3 Аналитика
- Интеграция с Google Analytics
- Логирование действий пользователей
- Метрики производительности

---

## План миграции (Поэтапный)

### Этап 1: Подготовка (1-2 дня)
- [ ] Создать Vite проект в папке `frontend/`
- [ ] Настроить TypeScript
- [ ] Настроить ESLint + Prettier
- [ ] Создать Docker конфигурацию

### Этап 2: Backend (3-5 дней)
- [ ] Мигрировать Sanic → FastAPI
- [ ] Добавить Pydantic схемы
- [ ] Настроить Alembic
- [ ] Написать тесты для API

### Этап 3: Frontend (5-7 дней)
- [ ] Перенести компоненты в TypeScript
- [ ] Разбить монолит на модули
- [ ] Интегрировать TanStack Query
- [ ] Заменить CSS на Tailwind
- [ ] Написать тесты

### Этап 4: Интеграция (2-3 дня)
- [ ] Настроить proxy в Vite
- [ ] Протестировать end-to-end
- [ ] Настроить CI/CD
- [ ] Документация API

### Этап 5: Деплой (1-2 дня)
- [ ] Собрать production build
- [ ] Настроить nginx
- [ ] Мониторинг и логи

---

## Риски и митигация

| Риск | Вероятность | Влияние | Митигация |
|------|-------------|---------|-----------|
| Потеря данных при миграции | Средняя | Высокое | Бэкапы, поэтапная миграция |
| Несовместимость API | Низкая | Среднее | Версионирование API |
| Долгая адаптация команды | Средняя | Среднее | Документация, обучение |
| Регрессия функционала | Средняя | Высокое | Полное покрытие тестами |

---

## Итоговая структура проекта

```
menu_app/
├── backend/                    # Python backend
│   ├── src/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   └── schemas/
│   │   ├── services/
│   │   ├── models/
│   │   └── db/
│   │       └── repositories/
│   ├── tests/
│   ├── alembic/
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── types/
│   │   └── App.tsx
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── Dockerfile
│
├── docker-compose.yml
├── .github/
│   └── workflows/
│       └── ci.yml
└── docs/
    ├── API.md
    ├── ARCHITECTURE.md
    └── DEPLOYMENT.md
```

---

## Заключение

Этот план рефакторинга трансформирует приложение из прототипа в production-ready решение с:

1. **Современным стеком**: FastAPI + React 18 + TypeScript
2. **Качественным кодом**: Модульность, типизация, тесты
3. **DevOps культурой**: Docker, CI/CD, мониторинг
4. **Масштабируемостью**: Готовность к росту нагрузки
5. **Поддерживаемостью**: Чистая архитектура, документация

Ожидаемый срок реализации: **2-3 недели** для полного рефакторинга.
