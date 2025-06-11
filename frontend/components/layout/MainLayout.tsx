import React, { useState, ReactNode, useEffect } from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import { Sidebar } from './Sidebar';
import { Topbar } from './Topbar';
import { useAppContext } from '../../hooks/useAppContext';
import { SIDENAV_ITEMS } from '../../constants';
import { useLanguage } from '../../hooks/useLanguage';
import { Spinner } from '../ui/Spinner';

interface MainLayoutProps {
  children?: ReactNode; // Allow children for non-Outlet usage if needed
}

export const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { setPageTitle, isLoading, error } = useAppContext();
  const { t } = useLanguage();
  const location = useLocation(); // from react-router-dom

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  useEffect(() => {
    const currentRoutedPath = location.pathname;
    const activeItem = SIDENAV_ITEMS.find(item => item.path === currentRoutedPath);
    
    if (activeItem) {
      setPageTitle(t(activeItem.labelKey, 'sidebar'));
    }
  }, [location.pathname, setPageTitle, t]);


  return (
    <div className="flex h-screen bg-neutral-100 dark:bg-neutral-950">
      <Sidebar isOpen={sidebarOpen} toggleSidebar={toggleSidebar} />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Topbar toggleSidebar={toggleSidebar} />
        <main className="flex-1 overflow-x-hidden overflow-y-auto p-4 md:p-6 lg:p-8 animate-fade-in">
          {isLoading && (
            <div className="fixed inset-0 bg-neutral-900 bg-opacity-30 backdrop-blur-sm flex items-center justify-center z-[100]">
              <Spinner size="lg" />
            </div>
          )}
          {error && (
             <div className="mb-6 p-4 bg-red-100 dark:bg-red-800/30 border border-red-300 dark:border-red-500/50 text-red-700 dark:text-red-300 rounded-lg shadow-md">
              <strong className="font-semibold">{t('error')}:</strong> {error}
            </div>
          )}
          {children || <Outlet />}
        </main>
      </div>
    </div>
  );
};