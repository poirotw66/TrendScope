import React, { ReactNode, useEffect } from 'react';
import { XIcon } from '../../constants';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: ReactNode;
  footer?: ReactNode;
  size?: 'sm' | 'md' | 'lg' | 'xl' | '2xl';
}

export const Modal: React.FC<ModalProps> = ({ isOpen, onClose, title, children, footer, size = 'md' }) => {
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [isOpen]);

  if (!isOpen) return null;

  const sizeClasses = {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-lg',
    xl: 'max-w-xl',
    '2xl': 'max-w-2xl',
  };

  return (
    <div
      className="fixed inset-0 z-[999] flex items-center justify-center bg-black/50 backdrop-blur-sm p-4 transition-opacity duration-300"
      onClick={onClose}
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
    >
      <div
        className={`bg-white dark:bg-neutral-800/95 dark:backdrop-blur-xl rounded-xl shadow-2xl w-full ${sizeClasses[size]} m-4 transform transition-all duration-300 ease-out animate-modal-appear flex flex-col max-h-[90vh]`}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between px-6 py-4 border-b border-neutral-200 dark:border-neutral-700/80">
          <h3 id="modal-title" className="text-xl font-semibold text-neutral-800 dark:text-neutral-100">{title}</h3>
          <button
            onClick={onClose}
            className="p-1.5 rounded-full text-neutral-500 hover:text-neutral-700 dark:text-neutral-400 dark:hover:text-neutral-200 hover:bg-neutral-100 dark:hover:bg-neutral-700/60 transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500/50"
            aria-label="Close modal"
          >
            <XIcon className="w-5 h-5" />
          </button>
        </div>
        <div className="p-6 overflow-y-auto flex-grow">
          {children}
        </div>
        {footer && (
          <div className="px-6 py-4 border-t border-neutral-200 dark:border-neutral-700/80 flex justify-end space-x-3 bg-neutral-50 dark:bg-neutral-800/50 rounded-b-xl">
            {footer}
          </div>
        )}
      </div>
    </div>
  );
};