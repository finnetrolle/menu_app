import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Layout } from './components/Layout';
import { DishesPage } from './pages/DishesPage';
import { IngredientsPage } from './pages/IngredientsPage';
import { AddDishPage } from './pages/AddDishPage';
import { EditDishPage } from './pages/EditDishPage';
import { MenuPlannerPage } from './pages/MenuPlannerPage';
import { ToastProvider } from './components/ui/toast';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      retry: 1,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ToastProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Layout />}>
              <Route index element={<MenuPlannerPage />} />
              <Route path="dishes" element={<DishesPage />} />
              <Route path="ingredients" element={<IngredientsPage />} />
              <Route path="add-dish" element={<AddDishPage />} />
              <Route path="edit-dish/:id" element={<EditDishPage />} />
              <Route path="*" element={<div className="text-center py-8 text-red-600">Страница не найдена</div>} />
            </Route>
          </Routes>
        </BrowserRouter>
      </ToastProvider>
    </QueryClientProvider>
  );
}

export default App;
