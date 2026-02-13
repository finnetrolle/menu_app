import { useState, useMemo } from 'react';
import type { Ingredient, SortConfig } from '../types';
import { ActionMenu } from './ui/ActionMenu';

interface IngredientTableProps {
  ingredients: Ingredient[];
  onEdit?: (ingredient: Ingredient) => void;
  onDelete?: (id: number) => void;
}

export function IngredientTable({ ingredients, onEdit, onDelete }: IngredientTableProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [sortConfig, setSortConfig] = useState<SortConfig>({ key: null, direction: 'asc' });

  const filteredIngredients = useMemo(() => {
    let filtered = [...ingredients];
    
    if (searchQuery.length >= 2) {
      filtered = filtered.filter((ing) =>
        ing.name.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }
    
    return filtered;
  }, [ingredients, searchQuery]);

  const sortedIngredients = useMemo(() => {
    let sorted = [...filteredIngredients];
    
    if (sortConfig.key !== null) {
      sorted.sort((a, b) => {
        let aValue: string | number = a[sortConfig.key as keyof Ingredient] as string | number;
        let bValue: string | number = b[sortConfig.key as keyof Ingredient] as string | number;
        
        // Handle nested nutrition properties
        if (sortConfig.key === 'name') {
          aValue = a.name.toLowerCase();
          bValue = b.name.toLowerCase();
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
  }, [filteredIngredients, sortConfig]);

  const requestSort = (key: keyof Ingredient) => {
    let direction: 'asc' | 'desc' = 'asc';
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });
  };

  const getSortIndicator = (key: keyof Ingredient) => {
    if (sortConfig.key !== key) return null;
    return sortConfig.direction === 'asc' ? ' ↑' : ' ↓';
  };

  return (
    <div className="space-y-4">
      {/* Search */}
      <div className="flex gap-4">
        <input
          type="text"
          placeholder="Поиск ингредиентов (мин. 2 символа)..."
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
                className="table-header"
              >
                Название{getSortIndicator('name')}
              </th>
              <th
                onClick={() => requestSort('id')}
                className="table-header"
              >
                ID{getSortIndicator('id')}
              </th>
              <th className="table-header">Калории</th>
              <th className="table-header">Белки</th>
              <th className="table-header">Жиры</th>
              <th className="table-header">Углеводы</th>
              {(onEdit || onDelete) && <th className="table-header">Действия</th>}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {sortedIngredients.map((ingredient) => (
              <tr key={ingredient.id} className="hover:bg-gray-50">
                <td className="table-cell font-medium">{ingredient.name}</td>
                <td className="table-cell text-gray-500">{ingredient.id}</td>
                <td className="table-cell">{ingredient.nutrition.calories}</td>
                <td className="table-cell">
                  <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs">
                    {ingredient.nutrition.proteins}г
                  </span>
                </td>
                <td className="table-cell">
                  <span className="px-2 py-1 bg-yellow-100 text-yellow-800 rounded text-xs">
                    {ingredient.nutrition.fats}г
                  </span>
                </td>
                <td className="table-cell">
                  <span className="px-2 py-1 bg-green-100 text-green-800 rounded text-xs">
                    {ingredient.nutrition.carbohydrates}г
                  </span>
                </td>
                {(onEdit || onDelete) && (
                  <td className="table-cell">
                    <ActionMenu
                      items={[
                        ...(onEdit
                          ? [{ label: 'Редактировать', onClick: () => onEdit(ingredient) }]
                          : []),
                        ...(onDelete
                          ? [{ label: 'Удалить', onClick: () => onDelete(ingredient.id), className: 'text-red-600' }]
                          : []),
                      ]}
                    />
                  </td>
                )}
              </tr>
            ))}
          </tbody>
        </table>

        {sortedIngredients.length === 0 && (
          <div className="text-center py-8 text-gray-500">
            {searchQuery.length >= 2 
              ? 'Ингредиенты не найдены' 
              : 'Введите минимум 2 символа для поиска'}
          </div>
        )}
      </div>
    </div>
  );
}
