// Nutrition information interface
export interface Nutrition {
  calories: number;
  proteins: number;
  fats: number;
  carbohydrates: number;
}

// Ingredient interface
export interface Ingredient {
  id: number;
  name: string;
  nutrition: Nutrition;
}

// Ingredient in dish with amount
export interface IngredientInDish {
  name: string;
  amount: number;
  unit: string;
  calories?: number;
  proteins?: number;
  fats?: number;
  carbohydrates?: number;
}

// Dish interface
export interface Dish {
  id: number;
  name: string;
  weight_g: number;
  energy_kcal: number;
  protein_g: number;
  carbohydrates_g: number;
  fat_g: number;
}

// Dish details with ingredients
export interface DishDetails {
  id: number;
  name: string;
  ingredients: IngredientInDish[];
}

// Goals interface
export interface Goals {
  protein: number;
  fat: number;
  carbohydrates: number;
  calories: number;
}

// Selected dish for menu calculation
export interface SelectedDish {
  id: number;
  portions: number;
}

// Menu processing result
export interface MenuResult {
  ingredients: Record<string, { amount: number; unit: string }>;
}

// API Response types
export interface ApiResponse<T> {
  status: 'success' | 'error';
  data?: T;
  error?: string;
}

// Sort configuration
export interface SortConfig {
  key: keyof Dish | keyof Ingredient | null;
  direction: 'asc' | 'desc';
}
