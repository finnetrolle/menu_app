import { useState, useMemo } from 'react';
import { useDishes } from '../hooks/useDishes';
import { useGoals, useSetGoals } from '../hooks/useGoals';
import { menuApi } from '../services/api';
import { NutritionProgress } from '../components/NutritionProgress';
import { LoadingSpinner } from '../components/ui/LoadingSpinner';
import type { Dish, SelectedDish, Goals, MenuResult } from '../types';

type Step = 1 | 2| 3;

export function MenuPlannerPage() {
  const { data: dishes = [], isLoading: dishesLoading } = useDishes();
  const { data: goals, isLoading: goalsLoading } = useGoals();
  const setGoals = useSetGoals();
  
  const [currentStep, setCurrentStep] = useState<Step>(1);
  const [tempGoals, setTempGoals] = useState<Goals>({
    protein: 0,
    fat: 0,
    carbohydrates: 0,
    calories: 0,
  });
  const [selectedDishes, setSelectedDishes] = useState<SelectedDish[]>([]);
  const [menuResult, setMenuResult] = useState<MenuResult | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  // Initialize temp goals from server
  useMemo(() => {
    if (goals) {
      setTempGoals(goals);
    }
  }, [goals]);

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

  const handleGoalsSubmit = async () => {
    await setGoals.mutateAsync(tempGoals);
    setCurrentStep(2);
  };

  const handleGenerateLists = async () => {
    setIsProcessing(true);
    try {
      const result = await menuApi.process(selectedDishes);
      setMenuResult(result);
      setCurrentStep(3);
    } catch (error) {
      console.error('Failed to process menu:', error);
      alert('Ошибка при обработке меню');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleStartOver = () => {
    setSelectedDishes([]);
    setMenuResult(null);
    setCurrentStep(1);
  };

  if (dishesLoading || goalsLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Progress Steps */}
      <div className="flex items-center justify-center mb-8">
        {[1, 2, 3].map((step) => (
          <div key={step} className="flex items-center">
            <div
              className={`w-10 h-10 rounded-full flex items-center justify-center font-semibold ${
                currentStep >= step
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-200 text-gray-600'
              }`}
            >
              {step}
            </div>
            {step <3 && (
              <div
                className={`w-20 h-1 ${
                  currentStep > step ? 'bg-blue-600' : 'bg-gray-200'
                }`}
              />
            )}
          </div>
        ))}
      </div>

      {/* Step 1: Goals Input */}
      {currentStep === 1 && (
        <div className="card">
          <h2 className="text-xl font-bold mb-6">Шаг1: Укажите ваши цели КБЖУ</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Белки (г)
              </label>
              <input
                type="number"
                min="0"
                value={tempGoals.protein}
                onChange={(e) => setTempGoals({ ...tempGoals, protein: parseFloat(e.target.value) || 0 })}
                className="input"
                placeholder="Например: 150"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Жиры (г)
              </label>
              <input
                type="number"
                min="0"
                value={tempGoals.fat}
                onChange={(e) => setTempGoals({ ...tempGoals, fat: parseFloat(e.target.value) || 0 })}
                className="input"
                placeholder="Например: 65"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Углеводы (г)
              </label>
              <input
                type="number"
                min="0"
                value={tempGoals.carbohydrates}
                onChange={(e) => setTempGoals({ ...tempGoals, carbohydrates: parseFloat(e.target.value) || 0 })}
                className="input"
                placeholder="Например: 250"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Калории (ккал)
              </label>
              <input
                type="number"
                min="0"
                value={tempGoals.calories}
                onChange={(e) => setTempGoals({ ...tempGoals, calories: parseFloat(e.target.value) || 0 })}
                className="input"
                placeholder="Например: 2000"
              />
            </div>
          </div>

          <div className="mt-6 flex justify-end">
            <button
              onClick={handleGoalsSubmit}
              disabled={tempGoals.protein === 0 && tempGoals.fat === 0 && tempGoals.carbohydrates === 0}
              className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Далее →
            </button>
          </div>
        </div>
      )}

      {/* Step 2: Dish Selection */}
      {currentStep === 2 && (
        <div className="space-y-6">
          <div className="card">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold">Шаг 2: Выберите блюда</h2>
              <button
                onClick={() => setCurrentStep(1)}
                className="text-blue-600 hover:text-blue-800"
              >
                ← Изменить цели
              </button>
            </div>
            
            {/* Current Goals Display */}
            <div className="bg-blue-50 p-3 rounded-lg mb-4">
              <div className="text-sm text-gray-600">
                <strong>Ваши цели:</strong> Б: {goals?.protein}г | Ж: {goals?.fat}г | У: {goals?.carbohydrates}г | Ккал: {goals?.calories}
              </div>
            </div>

            {/* Search */}
            <input
              type="text"
              placeholder="Поиск блюд..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="input mb-4"
            />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Dishes List */}
            <div className="lg:col-span-2">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {filteredDishes.map((dish) => {
                  const isSelected = selectedDishes.some((d) => d.id === dish.id);
                  const selectedDish = selectedDishes.find((d) => d.id === dish.id);
                  
                  return (
                    <div
                      key={dish.id}
                      className={`card cursor-pointer transition-all ${
                        isSelected ? 'ring-2 ring-blue-500 bg-blue-50' : 'hover:shadow-md'
                      }`}
                      onClick={() => toggleDishSelection(dish)}
                    >
                      <div className="flex justify-between items-start">
                        <div>
                          <h3 className="font-semibold">{dish.name}</h3>
                          <p className="text-sm text-gray-500">{dish.weight_g}г</p>
                        </div>
                        <div className="text-right text-sm">
                          <div>{dish.energy_kcal} ккал</div>
                          <div className="text-gray-500">
                            Б: {dish.protein_g}г | Ж: {dish.fat_g}г | У: {dish.carbohydrates_g}г
                          </div>
                        </div>
                      </div>
                      
                      {isSelected && selectedDish && (
                        <div className="mt-3 pt-3 border-t" onClick={(e) => e.stopPropagation()}>
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

            {/* Nutrition Progress */}
            <div className="lg:col-span-1">
              <NutritionProgress current={currentNutrients} goals={goals || tempGoals} />
              
              {selectedDishes.length > 0 && (
                <div className="mt-4 card">
                  <h4 className="font-medium mb-2">Выбрано блюд: {selectedDishes.length}</h4>
                </div>
              )}
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex justify-between">
            <button
              onClick={() => setCurrentStep(1)}
              className="btn-secondary"
            >
              ← Назад
            </button>
            <button
              onClick={handleGenerateLists}
              disabled={selectedDishes.length === 0 || isProcessing}
              className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isProcessing ? 'Обработка...' : 'Составить списки блюд и покупок →'}
            </button>
          </div>
        </div>
      )}

      {/* Step 3: Results */}
      {currentStep === 3 && menuResult && (
        <div className="space-y-6">
          <div className="card">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold">Шаг 3: Ваши списки</h2>
              <button
                onClick={handleStartOver}
                className="btn-secondary"
              >
                Начать заново
              </button>
            </div>
          </div>

          {/* Total Nutrition Summary */}
          <div className="card">
            <h3 className="text-lg font-semibold mb-4">Итого КБЖУ</h3>
            <NutritionProgress 
              current={menuResult.total_nutrition} 
              goals={goals || tempGoals} 
            />
          </div>

          {/* Selected Dishes List */}
          <div className="card">
            <h3 className="text-lg font-semibold mb-4">Список блюд</h3>
            <div className="overflow-x-auto">
              <table className="min-w-full">
                <thead>
                  <tr className="border-b">
                    <th className="text-left py-2">Блюдо</th>
                    <th className="text-center py-2">Количество</th>
                  </tr>
                </thead>
                <tbody>
                  {menuResult.dishes.map((dish) => (
                    <tr key={dish.id} className="border-b">
                      <td className="py-2">{dish.name}</td>
                      <td className="text-center py-2">{dish.portions} порций</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Shopping List */}
          <div className="card">
            <h3 className="text-lg font-semibold mb-4">Список покупок</h3>
            <div className="overflow-x-auto">
              <table className="min-w-full">
                <thead>
                  <tr className="border-b">
                    <th className="text-left py-2">Ингредиент</th>
                    <th className="text-right py-2">Количество</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.entries(menuResult.ingredients)
                    .sort(([a], [b]) => a.localeCompare(b))
                    .map(([name, data]) => (
                      <tr key={name} className="border-b">
                        <td className="py-2">{name}</td>
                        <td className="text-right py-2">
                          {data.amount.toFixed(1)} {data.unit}
                        </td>
                      </tr>
                    ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex justify-between">
            <button
              onClick={() => setCurrentStep(2)}
              className="btn-secondary"
            >
              ← Изменить выбор
            </button>
            <button
              onClick={handleStartOver}
              className="btn-primary"
            >
              Начать заново
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
