import type { Goals } from '../types';

interface NutritionProgressProps {
  current: {
    protein: number;
    fat: number;
    carbohydrates: number;
    calories: number;
  };
  goals: Goals;
}

function getPercentageClass(value: number): string {
  if (value < 20) return 'bg-green-100 text-green-800';
  if (value < 40) return 'bg-blue-100 text-blue-800';
  if (value < 60) return 'bg-yellow-100 text-yellow-800';
  if (value < 80) return 'bg-orange-100 text-orange-800';
  return 'bg-red-100 text-red-800';
}

export function NutritionProgress({ current, goals }: NutritionProgressProps) {
  const nutrients = [
    { key: 'protein', label: 'Белки', current: current.protein, goal: goals.protein, unit: 'г', color: 'bg-blue-500' },
    { key: 'fat', label: 'Жиры', current: current.fat, goal: goals.fat, unit: 'г', color: 'bg-yellow-500' },
    { key: 'carbohydrates', label: 'Углеводы', current: current.carbohydrates, goal: goals.carbohydrates, unit: 'г', color: 'bg-green-500' },
    { key: 'calories', label: 'Калории', current: current.calories, goal: goals.calories, unit: 'ккал', color: 'bg-purple-500' },
  ];

  return (
    <div className="card">
      <h3 className="text-lg font-semibold mb-4">Питательная ценность</h3>
      
      <div className="space-y-4">
        {nutrients.map(({ key, label, current: curr, goal, unit, color }) => {
          const percentage = goal > 0 ? Math.round((curr / goal) * 100) : 0;
          const displayPercentage = Math.min(percentage, 100);
          
          return (
            <div key={key}>
              <div className="flex justify-between items-center mb-1">
                <span className="text-sm font-medium text-gray-700">{label}</span>
                <span className="text-sm text-gray-500">
                  {curr.toFixed(1)} / {goal} {unit}
                </span>
              </div>
              
              <div className="w-full bg-gray-200 rounded-full h-2.5">
                <div
                  className={`${color} h-2.5 rounded-full transition-all duration-300`}
                  style={{ width: `${displayPercentage}%` }}
                />
              </div>
              
              <div className="flex justify-end mt-1">
                <span className={`text-xs px-2 py-0.5 rounded ${getPercentageClass(percentage)}`}>
                  {percentage}%
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
