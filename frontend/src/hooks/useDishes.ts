import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { dishesApi } from '../services/api';
import type { Dish, DishDetails } from '../types';

// Query keys
export const dishesKeys = {
  all: ['dishes'] as const,
  detail: (id: number) => ['dishes', id] as const,
};

// Hook for fetching all dishes
export function useDishes() {
  return useQuery<Dish[]>({
    queryKey: dishesKeys.all,
    queryFn: dishesApi.getAll,
  });
}

// Hook for fetching a single dish
export function useDish(id: number) {
  return useQuery<DishDetails>({
    queryKey: dishesKeys.detail(id),
    queryFn: () => dishesApi.getById(id),
    enabled: id > 0,
  });
}

// Hook for creating a new dish
export function useCreateDish() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: dishesApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: dishesKeys.all });
    },
  });
}

// Hook for updating a dish
export function useUpdateDish() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, ingredients }: { id: number; ingredients: { name: string; amount: number }[] }) =>
      dishesApi.update(id, ingredients),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: dishesKeys.all });
      queryClient.invalidateQueries({ queryKey: dishesKeys.detail(id) });
    },
  });
}

// Hook for deleting a dish
export function useDeleteDish() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: dishesApi.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: dishesKeys.all });
    },
  });
}
