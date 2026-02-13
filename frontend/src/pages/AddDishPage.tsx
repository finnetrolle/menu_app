import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCreateDish } from '../hooks/useDishes';
import { useIngredients } from '../hooks/useIngredients';
import { LoadingSpinner } from '../components/ui/LoadingSpinner';

interface DishIngredient {
  name: string;
  amount: number;
}

export function AddDishPage() {
  const navigate = useNavigate();
  const { data: ingredients = [], isLoading: ingredientsLoading } = useIngredients();
  const createDish = useCreateDish();

  const [dishName, setDishName] = useState('');
  const [dishIngredients, setDishIngredients] = useState<DishIngredient[]>([]);
  const [selectedIngredient, setSelectedIngredient] = useState('');
  const [selectedAmount, setSelectedAmount] = useState(100);
  const [searchQuery, setSearchQuery] = useState('');

  const filteredIngredients = ingredients.filter((ing) =>
    ing.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleAddIngredient = () => {
    if (!selectedIngredient || selectedAmount <= 0) return;

    // Check if ingredient already added
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
  };

  const handleRemoveIngredient = (name: string) => {
    setDishIngredients(dishIngredients.filter((i) => i.name !== name));
  };

  const handleUpdateAmount = (name: string, amount: number) => {
    setDishIngredients(
      dishIngredients.map((i) => (i.name === name ? { ...i, amount } : i))
    );
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!dishName.trim()) {
      alert('Введите название блюда');
      return;
    }

    if (dishIngredients.length === 0) {
      alert('Добавьте хотя бы один ингредиент');
      return;
    }

    try {
      await createDish.mutateAsync({
        name: dishName,
        ingredients: dishIngredients,
      });
      navigate('/');
    } catch (error) {
      alert('Ошибка при создании блюда');
      console.error(error);
    }
  };

  if (ingredientsLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center gap-4">
        <button
          onClick={() => navigate(-1)}
          className="btn-secondary"
        >
          ← Назад
        </button>
        <h1 className="text-2xl font-bold text-gray-800">Новое блюдо</h1>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Dish Name */}
        <div className="card">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Название блюда
          </label>
          <input
            type="text"
            value={dishName}
            onChange={(e) => setDishName(e.target.value)}
            placeholder="Введите название..."
            className="input"
            required
          />
        </div>

        {/* Add Ingredient */}
        <div className="card">
          <h3 className="text-lg font-medium mb-4">Добавить ингредиент</h3>

          <div className="space-y-4">
            {/* Search */}
            <input
              type="text"
              placeholder="Поиск ингредиента..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="input"
            />

            {/* Ingredient Select */}
            <div className="grid grid-cols-3 gap-4">
              <div className="col-span-2">
                <select
                  value={selectedIngredient}
                  onChange={(e) => setSelectedIngredient(e.target.value)}
                  className="input"
                >
                  <option value="">Выберите ингредиент</option>
                  {filteredIngredients.map((ing) => (
                    <option key={ing.id} value={ing.name}>
                      {ing.name}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <input
                  type="number"
                  value={selectedAmount}
                  onChange={(e) => setSelectedAmount(Number(e.target.value))}
                  min="1"
                  className="input"
                  placeholder="г"
                />
              </div>
            </div>

            <button
              type="button"
              onClick={handleAddIngredient}
              disabled={!selectedIngredient}
              className="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
            >
              + Добавить ингредиент
            </button>
          </div>
        </div>

        {/* Ingredients List */}
        {dishIngredients.length > 0 && (
          <div className="card">
            <h3 className="text-lg font-medium mb-4">Ингредиенты в блюде</h3>

            <div className="space-y-2">
              {dishIngredients.map((ing) => {
                const ingredientData = ingredients.find((i) => i.name === ing.name);
                return (
                  <div
                    key={ing.name}
                    className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                  >
                    <div className="flex-1">
                      <span className="font-medium">{ing.name}</span>
                      {ingredientData && (
                        <span className="text-sm text-gray-500 ml-2">
                          ({ingredientData.nutrition.calories} ккал/100г)
                        </span>
                      )}
                    </div>
                    <div className="flex items-center gap-2">
                      <input
                        type="number"
                        value={ing.amount}
                        onChange={(e) => handleUpdateAmount(ing.name, Number(e.target.value))}
                        min="1"
                        className="w-20 px-2 py-1 border rounded"
                      />
                      <span className="text-gray-500">г</span>
                      <button
                        type="button"
                        onClick={() => handleRemoveIngredient(ing.name)}
                        className="text-red-500 hover:text-red-700 ml-2"
                      >
                        ✕
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Total Nutrition */}
            <div className="mt-4 pt-4 border-t">
              <h4 className="font-medium mb-2">Итого на блюдо:</h4>
              <div className="grid grid-cols-4 gap-2 text-sm">
                {(() => {
                  const totals = { calories: 0, proteins: 0, fats: 0, carbohydrates: 0 };
                  dishIngredients.forEach((ing) => {
                    const data = ingredients.find((i) => i.name === ing.name);
                    if (data) {
                      const factor = ing.amount / 100;
                      totals.calories += data.nutrition.calories * factor;
                      totals.proteins += data.nutrition.proteins * factor;
                      totals.fats += data.nutrition.fats * factor;
                      totals.carbohydrates += data.nutrition.carbohydrates * factor;
                    }
                  });
                  return (
                    <>
                      <div className="p-2 bg-purple-50 rounded text-center">
                        <div className="font-medium">{Math.round(totals.calories)}</div>
                        <div className="text-gray-500">ккал</div>
                      </div>
                      <div className="p-2 bg-blue-50 rounded text-center">
                        <div className="font-medium">{totals.proteins.toFixed(1)}</div>
                        <div className="text-gray-500">Белки</div>
                      </div>
                      <div className="p-2 bg-yellow-50 rounded text-center">
                        <div className="font-medium">{totals.fats.toFixed(1)}</div>
                        <div className="text-gray-500">Жиры</div>
                      </div>
                      <div className="p-2 bg-green-50 rounded text-center">
                        <div className="font-medium">{totals.carbohydrates.toFixed(1)}</div>
                        <div className="text-gray-500">Углеводы</div>
                      </div>
                    </>
                  );
                })()}
              </div>
            </div>
          </div>
        )}

        {/* Submit */}
        <div className="flex gap-4">
          <button
            type="button"
            onClick={() => navigate(-1)}
            className="btn-secondary flex-1"
          >
            Отмена
          </button>
          <button
            type="submit"
            disabled={createDish.isPending}
            className="btn-primary flex-1 disabled:opacity-50"
          >
            {createDish.isPending ? 'Создание...' : 'Создать блюдо'}
          </button>
        </div>
      </form>
    </div>
  );
}
