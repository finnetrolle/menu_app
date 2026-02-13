import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Layout } from './components/Layout';
import { HomePage } from './pages/HomePage';
import { IngredientsPage } from './pages/IngredientsPage';
import { AddDishPage } from './pages/AddDishPage';
import { EditDishPage } from './pages/EditDishPage';

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
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<HomePage />} />
            <Route path="ingredients" element={<IngredientsPage />} />
            <Route path="add-dish" element={<AddDishPage />} />
            <Route path="edit-dish/:id" element={<EditDishPage />} />
            <Route path="*" element={<div className="text-center py-8 text-red-600">Страница не найдена</div>} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
