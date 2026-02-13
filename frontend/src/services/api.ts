import type { 
  Dish, 
  DishDetails, 
  Ingredient, 
  Goals, 
  SelectedDish, 
  MenuResult 
} from '../types';

const API_BASE = '/api';

// Helper function for API requests
async function fetchJson<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
    ...options,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ error: 'Unknown error' }));
    throw new Error(errorData.error || `API Error: ${response.statusText}`);
  }

  return response.json();
}

// Dishes API
export const dishesApi = {
  getAll: () => 
    fetchJson<Dish[]>(`${API_BASE}/dishes`),

  getById: (id: number) => 
    fetchJson<DishDetails>(`${API_BASE}/dish/${id}`),

  create: (data: { name: string; ingredients: { name: string; amount: number }[] }) =>
    fetchJson<{ status: string }>(`${API_BASE}/dish/new`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  update: (id: number, ingredients: { name: string; amount: number }[]) =>
    fetchJson<{ status: string }>(`${API_BASE}/dish/${id}`, {
      method: 'POST',
      body: JSON.stringify({ ingredients }),
    }),

  delete: (id: number) =>
    fetchJson<{ status: string }>(`${API_BASE}/dishes/${id}`, {
      method: 'DELETE',
    }),
};

// Ingredients API
export const ingredientsApi = {
  getAll: () => 
    fetchJson<Ingredient[]>(`${API_BASE}/ingredients`),

  create: (data: { name: string; nutrition: { calories: number; proteins: number; fats: number; carbohydrates: number } }) =>
    fetchJson<{ status: string }>(`${API_BASE}/ingredients`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  update: (id: number, nutrition: { calories: number; proteins: number; fats: number; carbohydrates: number }) =>
    fetchJson<{ status: string }>(`${API_BASE}/ingredients/${id}`, {
      method: 'PUT',
      body: JSON.stringify({ nutrition }),
    }),

  delete: (id: number) =>
    fetchJson<{ status: string }>(`${API_BASE}/ingredients/${id}`, {
      method: 'DELETE',
    }),
};

// Goals API
export const goalsApi = {
  get: () => 
    fetchJson<Goals>(`${API_BASE}/goals`),

  set: (goals: Goals) =>
    fetchJson<{ status: string; goals: Goals }>(`${API_BASE}/goals`, {
      method: 'POST',
      body: JSON.stringify(goals),
    }),
};

// Menu API
export const menuApi = {
  process: (dishes: SelectedDish[]) =>
    fetchJson<MenuResult>(`${API_BASE}/menu`, {
      method: 'POST',
      body: JSON.stringify({ dishes }),
    }),
};
