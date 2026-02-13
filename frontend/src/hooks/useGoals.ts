import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { goalsApi } from '../services/api';
import type { Goals } from '../types';

// Query keys
export const goalsKeys = {
  all: ['goals'] as const,
};

// Hook for fetching goals
export function useGoals() {
  return useQuery<Goals>({
    queryKey: goalsKeys.all,
    queryFn: goalsApi.get,
    initialData: {
      protein: 0,
      fat: 0,
      carbohydrates: 0,
      calories: 0,
    },
  });
}

// Hook for setting goals
export function useSetGoals() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: goalsApi.set,
    onSuccess: (data) => {
      queryClient.setQueryData(goalsKeys.all, data.goals);
    },
  });
}
