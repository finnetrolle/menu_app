import { useState } from 'react';
import { useIngredients, useDeleteIngredient } from '../hooks/useIngredients';
import { IngredientTable } from '../components/IngredientTable';
import { LoadingSpinner } from '../components/ui/LoadingSpinner';
import type { Ingredient } from '../types';

export function IngredientsPage() {
  const { data: ingredients = [], isLoading, error } = useIngredients();
  const deleteIngredient = useDeleteIngredient();
  
  const [editingIngredient, setEditingIngredient] = useState<Ingredient | null>(null);
  const [isAddingNew, setIsAddingNew] = useState(false);

  const handleEdit = (ingredient: Ingredient) => {
    setEditingIngredient(ingredient);
    setIsAddingNew(false);
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Вы уверены, что хотите удалить этот ингредиент?')) {
      deleteIngredient.mutate(id);
    }
  };

  const handleAddNew = () => {
    setIsAddingNew(true);
    setEditingIngredient(null);
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-8 text-red-600">
        Ошибка загрузки данных: {error.message}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-gray-800">Ингредиенты</h1>
        <button
          onClick={handleAddNew}
          className="btn-primary"
        >
          + Добавить ингредиент
        </button>
      </div>

      {/* Add/Edit Form Modal */}
      {(editingIngredient || isAddingNew) && (
        <IngredientForm
          ingredient={editingIngredient}
          onClose={() => {
            setEditingIngredient(null);
            setIsAddingNew(false);
          }}
        />
      )}

      {/* Ingredients Table */}
      <IngredientTable
        ingredients={ingredients}
        onEdit={handleEdit}
        onDelete={handleDelete}
      />
    </div>
  );
}

// Ingredient Form Component
interface IngredientFormProps {
  ingredient?: Ingredient | null;
  onClose: () => void;
}

function IngredientForm({ ingredient, onClose }: IngredientFormProps) {
  const [name, setName] = useState(ingredient?.name || '');
  const [calories, setCalories] = useState(ingredient?.nutrition.calories || 0);
  const [proteins, setProteins] = useState(ingredient?.nutrition.proteins || 0);
  const [fats, setFats] = useState(ingredient?.nutrition.fats || 0);
  const [carbohydrates, setCarbohydrates] = useState(ingredient?.nutrition.carbohydrates || 0);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: Implement save logic with mutation
    console.log({ name, calories, proteins, fats, carbohydrates });
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md">
        <h2 className="text-xl font-semibold mb-4">
          {ingredient ? 'Редактировать ингредиент' : 'Новый ингредиент'}
        </h2>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Название
            </label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="input"
              required
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Калории (ккал)
              </label>
              <input
                type="number"
                value={calories}
                onChange={(e) => setCalories(Number(e.target.value))}
                className="input"
                min="0"
                step="0.1"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Белки (г)
              </label>
              <input
                type="number"
                value={proteins}
                onChange={(e) => setProteins(Number(e.target.value))}
                className="input"
                min="0"
                step="0.1"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Жиры (г)
              </label>
              <input
                type="number"
                value={fats}
                onChange={(e) => setFats(Number(e.target.value))}
                className="input"
                min="0"
                step="0.1"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Углеводы (г)
              </label>
              <input
                type="number"
                value={carbohydrates}
                onChange={(e) => setCarbohydrates(Number(e.target.value))}
                className="input"
                min="0"
                step="0.1"
              />
            </div>
          </div>

          <div className="flex gap-3 pt-4">
            <button type="submit" className="btn-primary flex-1">
              Сохранить
            </button>
            <button
              type="button"
              onClick={onClose}
              className="btn-secondary flex-1"
            >
              Отмена
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
