/**
 * Add Dish Page
 * Uses shared DishForm component for consistency with EditDishPage.
 */

import { useNavigate } from 'react-router-dom';
import { useCreateDish } from '../hooks/useDishes';
import { useIngredients } from '../hooks/useIngredients';
import { DishForm } from '../components/DishForm';
import { useToast } from '../components/ui/toast';
import type { DishIngredient } from '../types';

export function AddDishPage() {
  const navigate = useNavigate();
  const { data: ingredients = [], isLoading: ingredientsLoading } = useIngredients();
  const createDish = useCreateDish();
  const toast = useToast();

  const handleSubmit = async (data: { name: string; ingredients: DishIngredient[] }) => {
    try {
      await createDish.mutateAsync({
        name: data.name,
        ingredients: data.ingredients,
      });
      toast.success(`Блюдо "${data.name}" успешно создано`);
      navigate('/dishes');
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Ошибка при создании блюда';
      toast.error(message);
      throw error;
    }
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <button
          onClick={() => navigate(-1)}
          className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50"
        >
          ← Назад
        </button>
        <h1 className="text-2xl font-bold text-gray-800">Новое блюдо</h1>
      </div>

      {/* Form Card */}
      <div className="bg-white rounded-lg shadow p-6">
        <DishForm
          onSubmit={handleSubmit}
          onCancel={() => navigate(-1)}
          ingredients={ingredients}
          ingredientsLoading={ingredientsLoading}
          isSubmitting={createDish.isPending}
        />
      </div>
    </div>
  );
}
