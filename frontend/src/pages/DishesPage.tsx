import { useNavigate } from 'react-router-dom';
import { useDishes, useDeleteDish } from '../hooks/useDishes';
import { DishTable } from '../components/DishTable';
import { LoadingSpinner } from '../components/ui/LoadingSpinner';

export function DishesPage() {
  const navigate = useNavigate();
  const { data: dishes = [], isLoading, error } = useDishes();
  const deleteDish = useDeleteDish();

  const handleEdit = (id: number) => {
    navigate(`/edit-dish/${id}`);
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Вы уверены, что хотите удалить это блюдо?')) {
      deleteDish.mutate(id);
    }
  };

  const handleAddNew = () => {
    navigate('/add-dish');
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
        <h1 className="text-2xl font-bold text-gray-800">Блюда</h1>
        <button
          onClick={handleAddNew}
          className="btn-primary"
        >
          + Добавить блюдо
        </button>
      </div>

      {/* Dishes Table */}
      <DishTable
        dishes={dishes}
        onEdit={handleEdit}
        onDelete={handleDelete}
      />
    </div>
  );
}
