import React, { useState, useRef, useEffect } from 'react';
import { useAppContext } from '../../hooks/useAppContext';
import { useTheme } from '../../hooks/useTheme';
import { useLanguage } from '../../hooks/useLanguage';
import { Theme, Language, Notification as NotificationType } from '../../types';
import { Button } from '../ui/Button';
import { 
  MenuIcon, SunIcon, MoonIcon, BellIcon, 
  LanguageIcon, CheckCircleIcon, XCircleIcon, ExclamationTriangleIcon, InformationCircleIcon, XIcon
} from '../../constants';

const TopbarButton: React.FC<{ onClick?: () => void; children: React.ReactNode; ariaLabel: string, className?: string }> = 
  ({ onClick, children, ariaLabel, className }) => (
  <button
    onClick={onClick}
    aria-label={ariaLabel}
    className={`p-2 rounded-full text-neutral-500 dark:text-neutral-400 hover:bg-neutral-100 dark:hover:bg-neutral-700/60 hover:text-primary-600 dark:hover:text-primary-300 focus:outline-none focus:ring-2 focus:ring-primary-500/50 focus:ring-offset-1 dark:focus:ring-offset-neutral-800 transition-colors duration-150 ${className}`}
  >
    {children}
  </button>
);

const NotificationItem: React.FC<{ notification: NotificationType; onMarkAsRead: (id: string) => void; t: (key: string, section?: string) => string; }> = ({ notification, onMarkAsRead, t }) => {
  const Icon = {
    info: InformationCircleIcon,
    success: CheckCircleIcon,
    warning: ExclamationTriangleIcon,
    error: XCircleIcon,
  }[notification.type];

  const colors = {
    info: 'text-blue-500',
    success: 'text-green-500',
    warning: 'text-yellow-500',
    error: 'text-red-500',
  }

  return (
    <div className={`p-3 border-b border-neutral-100 dark:border-neutral-700/80 last:border-b-0 hover:bg-neutral-50 dark:hover:bg-neutral-700/50 transition-colors`}>
      <div className="flex items-start space-x-3">
        <Icon className={`w-5 h-5 mt-0.5 shrink-0 ${colors[notification.type]}`} />
        <div className="flex-1">
          <p className="text-sm text-neutral-700 dark:text-neutral-200">{notification.message}</p>
          <p className="text-xs text-neutral-500 dark:text-neutral-400 mt-0.5">{new Date(notification.timestamp).toLocaleTimeString()}</p>
        </div>
        {!notification.read && (
          <button 
            onClick={() => onMarkAsRead(notification.id)}
            className="text-xs text-primary-500 hover:text-primary-700 dark:text-primary-400 dark:hover:text-primary-200 font-medium"
            title={t('markAsRead')}
          >
           {t('markAsRead')}
          </button>
        )}
      </div>
    </div>
  );
};


const DropdownMenu: React.FC<{ trigger: React.ReactNode; children: React.ReactNode; align?: 'left' | 'right' }> = ({ trigger, children, align = 'right' }) => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div className="relative inline-block text-left" ref={dropdownRef}>
      <div onClick={() => setIsOpen(!isOpen)}>{trigger}</div>
      {isOpen && (
        <div
          className={`absolute ${align === 'right' ? 'right-0' : 'left-0'} mt-2 w-72 origin-top-right bg-white dark:bg-neutral-800 rounded-xl shadow-2xl ring-1 ring-black ring-opacity-5 focus:outline-none z-50 overflow-hidden animate-modal-appear`}
        >
          {children}
        </div>
      )}
    </div>
  );
};


export const Topbar: React.FC<{ toggleSidebar: () => void }> = ({ toggleSidebar }) => {
  const { pageTitle, notifications, markNotificationAsRead, addNotification } = useAppContext();
  const { theme, toggleTheme } = useTheme();
  const { language, setLanguage, t } = useLanguage();
  
  const unreadNotificationsCount = notifications.filter(n => !n.read).length;

  // Example: Add a mock notification for demonstration
  // useEffect(() => {
  //   const timer = setTimeout(() => {
  //     addNotification({ message: 'New system update available.', type: 'info', timestamp: new Date() });
  //   }, 5000);
  //   return () => clearTimeout(timer);
  // }, [addNotification]);


  return (
    <header className="sticky top-0 z-20 flex items-center justify-between h-20 px-4 md:px-6 bg-white/80 dark:bg-neutral-900/80 backdrop-blur-md border-b border-neutral-200 dark:border-neutral-800/70 shadow-sm">
      <div className="flex items-center">
        <button
          onClick={toggleSidebar}
          className="p-2 mr-2 text-neutral-600 dark:text-neutral-300 rounded-full hover:bg-neutral-100 dark:hover:bg-neutral-700/60 lg:hidden"
          aria-label="Toggle sidebar"
        >
          <MenuIcon className="w-6 h-6" />
        </button>
        <h1 className="text-xl md:text-2xl font-semibold text-neutral-800 dark:text-neutral-100 truncate max-w-xs md:max-w-md lg:max-w-lg">
          {pageTitle}
        </h1>
      </div>

      <div className="flex items-center space-x-2 md:space-x-3">
        {/* Language Switcher */}
        <DropdownMenu
          trigger={
            <TopbarButton ariaLabel={t('language')}>
              <LanguageIcon className="w-5 h-5" />
            </TopbarButton>
          }
        >
           <div className="py-1">
            <button
              onClick={() => setLanguage(Language.EN)}
              className={`block w-full text-left px-4 py-2.5 text-sm ${language === Language.EN ? 'bg-primary-50 dark:bg-neutral-700 text-primary-600 dark:text-primary-300' : 'text-neutral-700 dark:text-neutral-200'} hover:bg-neutral-100 dark:hover:bg-neutral-700/80`}
            >
              English
            </button>
            <button
              onClick={() => setLanguage(Language.ZH_TW)}
              className={`block w-full text-left px-4 py-2.5 text-sm ${language === Language.ZH_TW ? 'bg-primary-50 dark:bg-neutral-700 text-primary-600 dark:text-primary-300' : 'text-neutral-700 dark:text-neutral-200'} hover:bg-neutral-100 dark:hover:bg-neutral-700/80`}
            >
              繁體中文
            </button>
          </div>
        </DropdownMenu>

        {/* Theme Toggle */}
        <TopbarButton onClick={toggleTheme} ariaLabel={t(theme === Theme.LIGHT ? 'darkMode' : 'lightMode')}>
          {theme === Theme.LIGHT ? <MoonIcon className="w-5 h-5" /> : <SunIcon className="w-5 h-5" />}
        </TopbarButton>

        {/* Notifications Bell */}
        <DropdownMenu
          trigger={
            <TopbarButton ariaLabel={t('notifications')}>
              <BellIcon className="w-5 h-5" />
              {unreadNotificationsCount > 0 && (
                <span className="absolute top-1 right-1 block h-2.5 w-2.5 rounded-full bg-red-500 ring-2 ring-white dark:ring-neutral-800" />
              )}
            </TopbarButton>
          }
        >
          <div className="px-4 py-3 border-b border-neutral-100 dark:border-neutral-700/80">
            <h4 className="text-sm font-semibold text-neutral-800 dark:text-neutral-100">{t('notifications')}</h4>
          </div>
          <div className="max-h-80 overflow-y-auto">
            {notifications.length === 0 ? (
              <p className="p-4 text-sm text-center text-neutral-500 dark:text-neutral-400">{t('noNotifications')}</p>
            ) : (
              notifications.map((n) => <NotificationItem key={n.id} notification={n} onMarkAsRead={markNotificationAsRead} t={t} />)
            )}
          </div>
        </DropdownMenu>
      </div>
    </header>
  );
};