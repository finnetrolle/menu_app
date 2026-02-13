import type { Dish } from '../types';

interface DishCardProps {
  dish: Dish;
  onSelect?: (dish: Dish) => void;
  onEdit?: (id: number) => void;
  onDelete?: (id: number) => void;
  isSelected?: boolean;
}

export function DishCard({ dish, onSelect, onEdit, onDelete, isSelected }: DishCardProps) {
  return (
    <div 
      className={`card cursor-pointer ${isSelected ? 'ring-2 ring-primary-500' : ''}`}
      onClick={() => onSelect?.(dish)}
    >
      <div className="flex justify-between items-start">
        <h3 className="text-lg font-semibold text-gray-800">{dish.name}</h3>
        <span className="text-sm text-gray-500">{dish.weight_g}г</span>
      </div>
      
      <div className="mt-3 space-y-2">
        <div className="flex items-center justify-between">
          <span className="text-sm text-gray-600">Калории</span>
          <span className="font-medium">{dish.energy_kcal} ккал</span>
        </div>
        
        <div className="flex gap-2">
          <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs font-medium">
            Б: {dish.protein_g}г
          </span>
          <span className="px-2 py-1 bg-yellow-100 text-yellow-800 rounded text-xs font-medium">
            Ж: {dish.fat_g}г
          </span>
          <span className="px-2 py-1 bg-green-100 text-green-800 rounded text-xs font-medium">
            У: {dish.carbohydrates_g}г
          </span>
        </div>
      </div>

      {(onEdit || onDelete) && (
        <div className="mt-4 flex gap-2" onClick={(e) => e.stopPropagation()}>
          {onEdit && (
            <button
              onClick={() => onEdit(dish.id)}
              className="btn-secondary text-sm flex-1"
            >
              Редактировать
            </button>
          )}
          {onDelete && (
            <button
              onClick={() => onDelete(dish.id)}
              className="bg-red-100 hover:bg-red-200 text-red-800 font-medium py-1 px-3 rounded-lg transition-colors text-sm"
            >
              Удалить
            </button>
          )}
        </div>
      )}
    </div>
  );
}
