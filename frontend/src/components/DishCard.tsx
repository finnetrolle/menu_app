import type { Dish } from '../types';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';

interface DishCardProps {
  dish: Dish;
  onSelect?: (dish: Dish) => void;
  onEdit?: (id: number) => void;
  onDelete?: (id: number) => void;
  isSelected?: boolean;
}

export function DishCard({ dish, onSelect, onEdit, onDelete, isSelected }: DishCardProps) {
  return (
    <Card 
      className={`cursor-pointer hover:shadow-lg transition-shadow ${isSelected ? 'ring-2 ring-primary-500' : ''}`}
      onClick={() => onSelect?.(dish)}
    >
      <CardHeader className="pb-2">
        <div className="flex justify-between items-start">
          <CardTitle className="text-lg">{dish.name}</CardTitle>
          <span className="text-sm text-muted-foreground">{dish.weight_g}г</span>
        </div>
      </CardHeader>
      
      <CardContent>
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-sm text-muted-foreground">Калории</span>
            <span className="font-medium">{dish.energy_kcal} ккал</span>
          </div>
          
          <div className="flex gap-2">
            <Badge variant="protein">
              Б: {dish.protein_g}г
            </Badge>
            <Badge variant="fat">
              Ж: {dish.fat_g}г
            </Badge>
            <Badge variant="carbs">
              У: {dish.carbohydrates_g}г
            </Badge>
          </div>
        </div>
      </CardContent>

      {(onEdit || onDelete) && (
        <CardFooter className="gap-2" onClick={(e) => e.stopPropagation()}>
          {onEdit && (
            <Button
              variant="secondary"
              size="sm"
              className="flex-1"
              onClick={() => onEdit(dish.id)}
            >
              Редактировать
            </Button>
          )}
          {onDelete && (
            <Button
              variant="destructive"
              size="sm"
              onClick={() => onDelete(dish.id)}
            >
              Удалить
            </Button>
          )}
        </CardFooter>
      )}
    </Card>
  );
}
