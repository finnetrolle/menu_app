import { useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDishes, useDeleteDish } from '../hooks/useDishes';
import { useGoals } from '../hooks/useGoals';
import { DishCard } from '../components/DishCard';
import { NutritionProgress } from '../components/NutritionProgress';
import { LoadingSpinner } from '../components/ui/LoadingSpinner';
import type { Dish, SelectedDish } from '../types';

export function HomePage() {
  const navigate = useNavigate();
  const { data: dishes = [], isLoading, error } = useDishes();
  const { data: goals } = useGoals();
  const deleteDish = useDeleteDish();
  
  const [selectedDishes, setSelectedDishes] = useState<SelectedDish[]>([]);
  const [searchQuery, setSearchQuery] = useState('');

  const filteredDishes = useMemo(() => {
    if (searchQuery.length < 2) return dishes;
    return dishes.filter((dish) =>
      dish.name.toLowerCase().includes(searchQuery.toLowerCase())
    );
  }, [dishes, searchQuery]);

  const currentNutrients = useMemo(() => {
    const nutrients = { protein: 0, fat: 0, carbohydrates: 0, calories: 0 };
    
    selectedDishes.forEach(({ id, portions }) => {
      const dish = dishes.find((d) => d.id === id);
      if (dish) {
        nutrients.protein += dish.protein_g * portions;
        nutrients.fat += dish.fat_g * portions;
        nutrients.carbohydrates += dish.carbohydrates_g * portions;
        nutrients.calories += dish.energy_kcal * portions;
      }
    });
    
    return nutrients;
  }, [selectedDishes, dishes]);

  const toggleDishSelection = (dish: Dish) => {
    setSelectedDishes((prev) => {
      const existing = prev.find((d) => d.id === dish.id);
      if (existing) {
        return prev.filter((d) => d.id !== dish.id);
      }
      return [...prev, { id: dish.id, portions: 1 }];
    });
  };

  const updatePortions = (dishId: number, portions: number) => {
    setSelectedDishes((prev) =>
      prev.map((d) => (d.id === dishId ? { ...d, portions: Math.max(1, portions) } : d))
    );
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Вы уверены, что хотите удалить это блюдо?')) {
      deleteDish.mutate(id);
    }
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
        <h1 className="text-2xl font-bold text-gray-800">Меню</h1>
        <button
          onClick={() => navigate('/add-dish')}
          className="btn-primary"
        >
          + Добавить блюдо
        </button>
      </div>

      {/* Search */}
      <input
        type="text"
        placeholder="Поиск блюд..."
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        className="input"
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Dishes List */}
        <div className="lg:col-span-2">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {filteredDishes.map((dish) => {
              const isSelected = selectedDishes.some((d) => d.id === dish.id);
              const selectedDish = selectedDishes.find((d) => d.id === dish.id);
              
              return (
                <div key={dish.id}>
                  <DishCard
                    dish={dish}
                    isSelected={isSelected}
                    onSelect={toggleDishSelection}
                    onEdit={(id) => navigate(`/edit-dish/${id}`)}
                    onDelete={handleDelete}
                  />
                  
                  {isSelected && selectedDish && (
                    <div className="mt-2 p-2 bg-gray-50 rounded-lg">
                      <label className="text-sm text-gray-600 mr-2">
                        Порции:
                      </label>
                      <input
                        type="number"
                        min="1"
                        value={selectedDish.portions}
                        onChange={(e) => updatePortions(dish.id, parseInt(e.target.value) || 1)}
                        className="w-20 px-2 py-1 border rounded"
                      />
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          {filteredDishes.length === 0 && (
            <div className="text-center py-8 text-gray-500">
              Блюда не найдены
            </div>
          )}
        </div>

        {/* Nutrition Summary */}
        <div className="lg:col-span-1">
          <NutritionProgress current={currentNutrients} goals={goals} />
          
          {selectedDishes.length > 0 && (
            <div className="mt-4 card">
              <h4 className="font-medium mb-2">Выбранные блюда:</h4>
              <ul className="space-y-1 text-sm text-gray-600">
                {selectedDishes.map(({ id, portions }) => {
                  const dish = dishes.find((d) => d.id === id);
                  return dish ? (
                    <li key={id} className="flex justify-between">
                      <span>{dish.name}</span>
                      <span>×{portions}</span>
                    </li>
                  ) : null;
                })}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
