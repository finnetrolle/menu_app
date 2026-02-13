import { useState, useMemo } from 'react';
import type { Dish, SortConfig } from '../types';

interface DishTableProps {
  dishes: Dish[];
  onEdit?: (id: number) => void;
  onDelete?: (id: number) => void;
}

export function DishTable({ dishes, onEdit, onDelete }: DishTableProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [sortConfig, setSortConfig] = useState<SortConfig>({ key: null, direction: 'asc' });

  const filteredDishes = useMemo(() => {
    let filtered = [...dishes];
    
    if (searchQuery.length >= 2) {
      filtered = filtered.filter((dish) =>
        dish.name.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }
    
    return filtered;
  }, [dishes, searchQuery]);

  const sortedDishes = useMemo(() => {
    let sorted = [...filteredDishes];
    
    if (sortConfig.key !== null) {
      sorted.sort((a, b) => {
        let aValue: string | number;
        let bValue: string | number;
        
        const key = sortConfig.key as keyof Dish;
        
        if (key === 'name') {
          aValue = a.name.toLowerCase();
          bValue = b.name.toLowerCase();
        } else {
          aValue = a[key] as number;
          bValue = b[key] as number;
        }
        
        if (aValue < bValue) {
          return sortConfig.direction === 'asc' ? -1 : 1;
        }
        if (aValue > bValue) {
          return sortConfig.direction === 'asc' ? 1 : -1;
        }
        return 0;
      });
    }
    
    return sorted;
  }, [filteredDishes, sortConfig]);

  const requestSort = (key: keyof Dish) => {
    let direction: 'asc' | 'desc' = 'asc';
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });
  };

  const getSortIndicator = (key: keyof Dish) => {
    if (sortConfig.key !== key) return null;
    return sortConfig.direction === 'asc' ? ' ↑' : ' ↓';
  };

  return (
    <div className="space-y-4">
      {/* Search */}
      <div className="flex gap-4">
        <input
          type="text"
          placeholder="Поиск блюд (мин. 2 символа)..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="input flex-1"
        />
      </div>

      {/* Table */}
      <div className="overflow-x-auto rounded-lg border border-gray-200">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th
                onClick={() => requestSort('name')}
                className="table-header cursor-pointer hover:bg-gray-100"
              >
                Название{getSortIndicator('name')}
              </th>
              <th
                onClick={() => requestSort('weight_g')}
                className="table-header cursor-pointer hover:bg-gray-100"
              >
                Вес{getSortIndicator('weight_g')}
              </th>
              <th
                onClick={() => requestSort('energy_kcal')}
                className="table-header cursor-pointer hover:bg-gray-100"
              >
                Калории{getSortIndicator('energy_kcal')}
              </th>
              <th
                onClick={() => requestSort('protein_g')}
                className="table-header cursor-pointer hover:bg-gray-100"
              >
                Белки{getSortIndicator('protein_g')}
              </th>
              <th
                onClick={() => requestSort('fat_g')}
                className="table-header cursor-pointer hover:bg-gray-100"
              >
                Жиры{getSortIndicator('fat_g')}
              </th>
              <th
                onClick={() => requestSort('carbohydrates_g')}
                className="table-header cursor-pointer hover:bg-gray-100"
              >
                Углеводы{getSortIndicator('carbohydrates_g')}
              </th>
              {(onEdit || onDelete) && <th className="table-header">Действия</th>}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {sortedDishes.map((dish) => (
              <tr key={dish.id} className="hover:bg-gray-50">
                <td className="table-cell font-medium">{dish.name}</td>
                <td className="table-cell text-gray-500">{dish.weight_g}г</td>
                <td className="table-cell">{dish.energy_kcal} ккал</td>
                <td className="table-cell">
                  <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs">
                    {dish.protein_g}г
                  </span>
                </td>
                <td className="table-cell">
                  <span className="px-2 py-1 bg-yellow-100 text-yellow-800 rounded text-xs">
                    {dish.fat_g}г
                  </span>
                </td>
                <td className="table-cell">
                  <span className="px-2 py-1 bg-green-100 text-green-800 rounded text-xs">
                    {dish.carbohydrates_g}г
                  </span>
                </td>
                {(onEdit || onDelete) && (
                  <td className="table-cell">
                    <div className="flex gap-2">
                      {onEdit && (
                        <button
                          onClick={() => onEdit(dish.id)}
                          className="text-primary-600 hover:text-primary-800 text-sm"
                        >
                          Редактировать
                        </button>
                      )}
                      {onDelete && (
                        <button
                          onClick={() => onDelete(dish.id)}
                          className="text-red-600 hover:text-red-800 text-sm"
                        >
                          Удалить
                        </button>
                      )}
                    </div>
                  </td>
                )}
              </tr>
            ))}
          </tbody>
        </table>

        {sortedDishes.length === 0 && (
          <div className="text-center py-8 text-gray-500">
            {searchQuery.length >= 2 
              ? 'Блюда не найдены' 
              : 'Введите минимум 2 символа для поиска'}
          </div>
        )}
      </div>
    </div>
  );
}
