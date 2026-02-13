/**
 * Simple toast notification system.
 * Can be replaced with sonner or react-hot-toast later.
 */

import { useState, useCallback, createContext, useContext, type ReactNode } from 'react';

interface Toast {
  id: string;
  type: 'success' | 'error' | 'info';
  message: string;
}

interface ToastContextType {
  toasts: Toast[];
  success: (message: string) => void;
  error: (message: string) => void;
  info: (message: string) => void;
  remove: (id: string) => void;
}

const ToastContext = createContext<ToastContextType | null>(null);

export function useToast() {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within a ToastProvider');
  }
  return context;
}

export function ToastProvider({ children }: { children: ReactNode }) {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const addToast = useCallback((type: Toast['type'], message: string) => {
    const id = Date.now().toString();
    setToasts((prev) => [...prev, { id, type, message }]);
    
    // Auto-remove after 4 seconds
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, 4000);
  }, []);

  const remove = useCallback((id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  const success = useCallback((message: string) => addToast('success', message), [addToast]);
  const error = useCallback((message: string) => addToast('error', message), [addToast]);
  const info = useCallback((message: string) => addToast('info', message), [addToast]);

  return (
    <ToastContext.Provider value={{ toasts, success, error, info, remove }}>
      {children}
      <ToastContainer toasts={toasts} remove={remove} />
    </ToastContext.Provider>
  );
}

function ToastContainer({ toasts, remove }: { toasts: Toast[]; remove: (id: string) => void }) {
  if (toasts.length === 0) return null;

  return (
    <div className="fixed top-4 right-4 z-50 flex flex-col gap-2">
      {toasts.map((toast) => (
        <div
          key={toast.id}
          className={`px-4 py-3 rounded-lg shadow-lg flex items-center gap-3 min-w-[300px] animate-slide-in ${
            toast.type === 'error'
              ? 'bg-red-600 text-white'
              : toast.type === 'success'
              ? 'bg-green-600 text-white'
              : 'bg-blue-600 text-white'
          }`}
        >
          <span className="flex-1">{toast.message}</span>
          <button
            onClick={() => remove(toast.id)}
            className="text-white/80 hover:text-white"
          >
            ✕
          </button>
        </div>
      ))}
    </div>
  );
}

// Export a simple toast object for direct use
export const toast = {
  success: (message: string) => {
    // This will be replaced with proper implementation via context
    console.log('[SUCCESS]', message);
  },
  error: (message: string) => {
    console.error('[ERROR]', message);
  },
  info: (message: string) => {
    console.log('[INFO]', message);
  },
};
