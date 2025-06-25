import React from 'react';
import { NavLink } from 'react-router-dom';
import { SIDENAV_GROUPS, APP_NAME, XIcon, NavItem, NavGroup } from '../../constants';
import { useLanguage } from '../../hooks/useLanguage';

interface SidebarProps {
  isOpen: boolean;
  toggleSidebar: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ isOpen, toggleSidebar }) => {
  const { t } = useLanguage();

  return (
    <>
      {/* Overlay for mobile */}
      {isOpen && (
        <div
          className="fixed inset-0 z-30 bg-black/30 backdrop-blur-sm lg:hidden"
          onClick={toggleSidebar}
        ></div>
      )}

      <aside
        className={`fixed top-0 left-0 z-40 h-screen bg-white dark:bg-neutral-900 text-neutral-800 dark:text-neutral-100 w-64 shadow-xl transform transition-transform duration-300 ease-in-out lg:translate-x-0 border-r border-neutral-200 dark:border-neutral-800 ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        } lg:static lg:inset-y-0 lg:flex lg:w-64 lg:flex-col`}
      >
        <div className="flex items-center justify-between h-20 px-6 border-b border-neutral-200 dark:border-neutral-800">
          <div className="flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 24 24" className="h-8 w-8 mr-3 text-primary-500">
              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 14H9V8h2v8zm4 0h-2V8h2v8z"/>
            </svg>
            <span className="text-2xl font-bold text-primary-600 dark:text-primary-400">{APP_NAME}</span>
          </div>
          <button onClick={toggleSidebar} className="lg:hidden text-neutral-500 dark:text-neutral-400 hover:text-primary-500 dark:hover:text-primary-400">
            <XIcon className="w-6 h-6" />
          </button>
        </div>
        <nav className="flex-1 p-4 space-y-2">
          {SIDENAV_GROUPS.map((group: NavGroup, groupIndex) => (
            <div key={group.groupKey || `group-${groupIndex}`} className="space-y-1.5">
              {/* 分組標題 */}
              {group.groupKey && (
                <div className="px-4 py-2">
                  <h3 className="text-xs font-semibold text-neutral-500 dark:text-neutral-400 uppercase tracking-wider">
                    {t(group.groupKey, 'sidebar')}
                  </h3>
                </div>
              )}

              {/* 分組項目 */}
              {group.items.map((item: NavItem) => (
                <NavLink
                  key={item.path}
                  to={item.path}
                  onClick={() => { if (window.innerWidth < 1024) toggleSidebar(); }}
                  className={({ isActive }) =>
                    `flex items-center px-4 py-3 rounded-lg text-base font-medium transition-all duration-150 group
                    ${
                      isActive
                        ? 'bg-primary-500 text-white shadow-md hover:bg-primary-600'
                        : 'text-neutral-600 dark:text-neutral-300 hover:bg-primary-50 dark:hover:bg-neutral-800 hover:text-primary-600 dark:hover:text-primary-300'
                    }`
                  }
                >
                  <item.icon className="w-5 h-5 mr-3 transition-colors duration-150 group-hover:text-primary-500" />
                  {t(item.labelKey, 'sidebar')}
                </NavLink>
              ))}

              {/* 分組間的分隔線（除了最後一組） */}
              {groupIndex < SIDENAV_GROUPS.length - 1 && group.groupKey && (
                <div className="pt-2">
                  <hr className="border-neutral-200 dark:border-neutral-700" />
                </div>
              )}
            </div>
          ))}
        </nav>
        <div className="p-6 border-t border-neutral-200 dark:border-neutral-800">
          <p className="text-xs text-neutral-500 dark:text-neutral-400">&copy; {new Date().getFullYear()} {APP_NAME}</p>
        </div>
      </aside>
    </>
  );
};