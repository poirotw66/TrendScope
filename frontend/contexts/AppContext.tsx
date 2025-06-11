
import React, { createContext, useState, ReactNode, useCallback } from 'react';
import { AppContextType, AppState, User, Notification } from '../types';

const initialState: AppState = {
  user: { name: 'Dev User' }, // Mock user
  isLoading: false,
  error: null,
  notifications: [],
  pageTitle: 'TrendScope',
};

export const AppContext = createContext<AppContextType | undefined>(undefined);

export const AppProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [state, setState] = useState<AppState>(initialState);

  const setUser = useCallback((user: User | null) => {
    setState((prevState) => ({ ...prevState, user }));
  }, []);

  const setLoading = useCallback((isLoading: boolean) => {
    setState((prevState) => ({ ...prevState, isLoading }));
  }, []);

  const setError = useCallback((error: string | null) => {
    setState((prevState) => ({ ...prevState, error }));
  }, []);

  const addNotification = useCallback((notification: Omit<Notification, 'id' | 'read'>) => {
    const newNotification: Notification = {
      ...notification,
      id: new Date().toISOString() + Math.random().toString(36).substring(2,9),
      read: false,
      timestamp: new Date(),
    };
    setState((prevState) => ({
      ...prevState,
      notifications: [newNotification, ...prevState.notifications.slice(0, 4)], // Keep max 5 notifications
    }));
  }, []);

  const markNotificationAsRead = useCallback((id: string) => {
    setState((prevState) => ({
      ...prevState,
      notifications: prevState.notifications.map((n) =>
        n.id === id ? { ...n, read: true } : n
      ),
    }));
  }, []);
  
  const setPageTitle = useCallback((title: string) => {
    setState(prevState => ({ ...prevState, pageTitle: title }));
    document.title = `${title} - TrendScope`;
  }, []);


  return (
    <AppContext.Provider
      value={{
        ...state,
        setUser,
        setLoading,
        setError,
        addNotification,
        markNotificationAsRead,
        setPageTitle,
      }}
    >
      {children}
    </AppContext.Provider>
  );
};
