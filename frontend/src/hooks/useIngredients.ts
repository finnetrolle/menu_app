import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { ingredientsApi } from '../services/api';
import type { Ingredient } from '../types';

// Query keys
export const ingredientsKeys = {
  all: ['ingredients'] as const,
};

// Hook for fetching all ingredients
export function useIngredients() {
  return useQuery<Ingredient[]>({
    queryKey: ingredientsKeys.all,
    queryFn: ingredientsApi.getAll,
  });
}

// Hook for creating a new ingredient
export function useCreateIngredient() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ingredientsApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ingredientsKeys.all });
    },
  });
}

// Hook for updating an ingredient
export function useUpdateIngredient() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, nutrition }: { id: number; nutrition: { calories: number; proteins: number; fats: number; carbohydrates: number } }) =>
      ingredientsApi.update(id, nutrition),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ingredientsKeys.all });
    },
  });
}

// Hook for deleting an ingredient
export function useDeleteIngredient() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ingredientsApi.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ingredientsKeys.all });
    },
  });
}
