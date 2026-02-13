/**
 * Shared dish form component.
 * Used by both AddDishPage and EditDishPage to reduce code duplication.
 */

import { useState, useMemo } from 'react';
import type { Ingredient, DishIngredient } from '../../types';

interface DishFormProps {
  /** Initial dish name (empty for create mode) */
  initialName?: string;
  /** Initial ingredients list */
  initialIngredients?: DishIngredient[];
  /** Callback when form is submitted */
  onSubmit: (data: { name: string; ingredients: DishIngredient[] }) => Promise<void>;
  /** Callback when cancel is clicked */
  onCancel: () => void;
  /** Whether the form is in edit mode */
  isEditMode?: boolean;
  /** Whether the form is submitting */
  isSubmitting?: boolean;
  /** List of available ingredients */
  ingredients: Ingredient[];
  /** Whether ingredients are loading */
  ingredientsLoading?: boolean;
}

export function DishForm({
  initialName = '',
  initialIngredients = [],
  onSubmit,
  onCancel,
  isEditMode = false,
  isSubmitting = false,
  ingredients = [],
  ingredientsLoading = false,
}: DishFormProps) {
  const [dishName, setDishName] = useState(initialName);
  const [dishIngredients, setDishIngredients] = useState<DishIngredient[]>(initialIngredients);
  const [selectedIngredient, setSelectedIngredient] = useState('');
  const [selectedAmount, setSelectedAmount] = useState(100);
  const [searchQuery, setSearchQuery] = useState('');
  const [errors, setErrors] = useState<{ name?: string; ingredients?: string }>({});

  const filteredIngredients = useMemo(() => {
    if (searchQuery.length < 1) return ingredients;
    return ingredients.filter((ing) =>
      ing.name.toLowerCase().includes(searchQuery.toLowerCase())
    );
  }, [ingredients, searchQuery]);

  const handleAddIngredient = () => {
    if (!selectedIngredient || selectedAmount <= 0) return;

    const existing = dishIngredients.find((i) => i.name === selectedIngredient);
    if (existing) {
      setDishIngredients(
        dishIngredients.map((i) =>
          i.name === selectedIngredient ? { ...i, amount: i.amount + selectedAmount } : i
        )
      );
    } else {
      setDishIngredients([...dishIngredients, { name: selectedIngredient, amount: selectedAmount }]);
    }

    setSelectedIngredient('');
    setSelectedAmount(100);
    setSearchQuery('');
    setErrors((prev) => ({ ...prev, ingredients: undefined }));
  };

  const handleRemoveIngredient = (name: string) => {
    setDishIngredients(dishIngredients.filter((i) => i.name !== name));
  };

  const handleUpdateAmount = (name: string, amount: number) => {
    if (amount <= 0) return;
    setDishIngredients(
      dishIngredients.map((i) => (i.name === name ? { ...i, amount } : i))
    );
  };

  const validate = (): boolean => {
    const newErrors: { name?: string; ingredients?: string } = {};

    if (!dishName.trim()) {
      newErrors.name = 'Введите название блюда';
    }

    if (dishIngredients.length === 0) {
      newErrors.ingredients = 'Добавьте хотя бы один ингредиент';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validate()) return;

    try {
      await onSubmit({ name: dishName.trim(), ingredients: dishIngredients });
    } catch (error) {
      // Error handling is done by the parent component
      throw error;
    }
  };

  if (ingredientsLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Dish Name */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Название блюда
        </label>
        <input
          type="text"
          value={dishName}
          onChange={(e) => {
            setDishName(e.target.value);
            setErrors((prev) => ({ ...prev, name: undefined }));
          }}
          className={`w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
            errors.name ? 'border-red-500' : 'border-gray-300'
          }`}
          placeholder="Например: Омлет с овощами"
          disabled={isEditMode} // Name cannot be changed in edit mode
        />
        {errors.name && (
          <p className="mt-1 text-sm text-red-600">{errors.name}</p>
        )}
      </div>

      {/* Ingredient Selection */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Добавить ингредиент
        </label>
        <div className="flex gap-2">
          <div className="flex-1 relative">
            <input
              type="text"
              placeholder="Поиск ингредиента..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            />
            {searchQuery && filteredIngredients.length > 0 && (
              <div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-lg shadow-lg max-h-48 overflow-y-auto">
                {filteredIngredients.slice(0, 10).map((ing) => (
                  <button
                    key={ing.id}
                    type="button"
                    onClick={() => {
                      setSelectedIngredient(ing.name);
                      setSearchQuery('');
                    }}
                    className="w-full px-3 py-2 text-left hover:bg-gray-100"
                  >
                    {ing.name}
                  </button>
                ))}
              </div>
            )}
          </div>
          <input
            type="number"
            min="1"
            value={selectedAmount}
            onChange={(e) => setSelectedAmount(parseInt(e.target.value) || 0)}
            className="w-24 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            placeholder="г"
          />
          <button
            type="button"
            onClick={handleAddIngredient}
            disabled={!selectedIngredient || selectedAmount <= 0}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Добавить
          </button>
        </div>
        {selectedIngredient && (
          <p className="mt-1 text-sm text-gray-500">
            Выбран: {selectedIngredient}
          </p>
        )}
      </div>

      {/* Selected Ingredients List */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Ингредиенты в блюде
        </label>
        {dishIngredients.length === 0 ? (
          <p className="text-gray-500 text-sm">Нет добавленных ингредиентов</p>
        ) : (
          <div className="space-y-2">
            {dishIngredients.map((ing) => (
              <div
                key={ing.name}
                className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg"
              >
                <span className="flex-1 font-medium">{ing.name}</span>
                <input
                  type="number"
                  min="1"
                  value={ing.amount}
                  onChange={(e) => handleUpdateAmount(ing.name, parseInt(e.target.value) || 1)}
                  className="w-20 px-2 py-1 border border-gray-300 rounded"
                />
                <span className="text-gray-500">г</span>
                <button
                  type="button"
                  onClick={() => handleRemoveIngredient(ing.name)}
                  className="text-red-600 hover:text-red-800"
                >
                  ✕
                </button>
              </div>
            ))}
          </div>
        )}
        {errors.ingredients && (
          <p className="mt-1 text-sm text-red-600">{errors.ingredients}</p>
        )}
      </div>

      {/* Total Weight */}
      {dishIngredients.length > 0 && (
        <div className="text-sm text-gray-600">
          Общий вес: {dishIngredients.reduce((sum, ing) => sum + ing.amount, 0)} г
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex gap-4 pt-4">
        <button
          type="button"
          onClick={onCancel}
          className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50"
          disabled={isSubmitting}
        >
          Отмена
        </button>
        <button
          type="submit"
          disabled={isSubmitting}
          className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isSubmitting 
            ? 'Сохранение...' 
            : isEditMode 
              ? 'Сохранить изменения' 
              : 'Создать блюдо'}
        </button>
      </div>
    </form>
  );
}
