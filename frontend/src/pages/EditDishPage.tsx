/**
 * Edit Dish Page
 * Uses shared DishForm component for consistency with AddDishPage.
 */

import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useDish, useUpdateDish, useDeleteDish } from '../hooks/useDishes';
import { useIngredients } from '../hooks/useIngredients';
import { DishForm } from '../components/DishForm';
import { useToast } from '../components/ui/toast';
import { LoadingSpinner } from '../components/ui/LoadingSpinner';
import type { DishIngredient } from '../types';

export function EditDishPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const dishId = Number(id);
  const toast = useToast();

  const { data: dish, isLoading: dishLoading } = useDish(dishId);
  const { data: ingredients = [], isLoading: ingredientsLoading } = useIngredients();
  const updateDish = useUpdateDish();
  const deleteDish = useDeleteDish();

  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  // Transform dish ingredients to DishIngredient format
  const initialIngredients: DishIngredient[] = dish?.ingredients?.map((ing) => ({
    name: ing.name,
    amount: ing.amount,
  })) || [];

  const handleSubmit = async (data: { name: string; ingredients: DishIngredient[] }) => {
    try {
      await updateDish.mutateAsync({
        id: dishId,
        ingredients: data.ingredients,
      });
      toast.success('Блюдо успешно обновлено');
      navigate('/dishes');
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Ошибка при обновлении блюда';
      toast.error(message);
      throw error;
    }
  };

  const handleDelete = async () => {
    try {
      await deleteDish.mutateAsync(dishId);
      toast.success('Блюдо успешно удалено');
      navigate('/dishes');
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Ошибка при удалении блюда';
      toast.error(message);
    }
  };

  if (dishLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (!dish) {
    return (
      <div className="max-w-2xl mx-auto">
        <div className="bg-white rounded-lg shadow p-6 text-center">
          <h2 className="text-xl font-bold text-gray-800 mb-4">Блюдо не найдено</h2>
          <button
            onClick={() => navigate('/dishes')}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Вернуться к списку блюд
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <button
            onClick={() => navigate(-1)}
            className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50"
          >
            ← Назад
          </button>
          <h1 className="text-2xl font-bold text-gray-800">
            Редактирование: {dish.name}
          </h1>
        </div>
        <button
          onClick={() => setShowDeleteConfirm(true)}
          className="px-4 py-2 text-red-600 hover:bg-red-50 rounded-lg"
        >
          🗑 Удалить
        </button>
      </div>

      {/* Form Card */}
      <div className="bg-white rounded-lg shadow p-6">
        <DishForm
          initialName={dish.name}
          initialIngredients={initialIngredients}
          onSubmit={handleSubmit}
          onCancel={() => navigate('/dishes')}
          isEditMode={true}
          ingredients={ingredients}
          ingredientsLoading={ingredientsLoading}
          isSubmitting={updateDish.isPending}
        />
      </div>

      {/* Delete Confirmation Modal */}
      {showDeleteConfirm && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-lg p-6 max-w-md w-full mx-4">
            <h3 className="text-lg font-bold text-gray-800 mb-2">
              Подтверждение удаления
            </h3>
            <p className="text-gray-600 mb-6">
              Вы уверены, что хотите удалить блюдо "{dish.name}"? Это действие нельзя отменить.
            </p>
            <div className="flex gap-4">
              <button
                onClick={() => setShowDeleteConfirm(false)}
                className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50"
              >
                Отмена
              </button>
              <button
                onClick={handleDelete}
                disabled={deleteDish.isPending}
                className="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50"
              >
                {deleteDish.isPending ? 'Удаление...' : 'Удалить'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
