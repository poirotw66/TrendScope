import React, { HTMLAttributes } from 'react';

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  title?: string;
  footer?: React.ReactNode;
  titleClassName?: string;
  bodyClassName?: string;
  footerClassName?: string;
}

export const Card: React.FC<CardProps> = ({ title, children, footer, className = '', titleClassName = '', bodyClassName = '', footerClassName = '', ...props }) => {
  return (
    <div
      className={`bg-white dark:bg-neutral-800/70 dark:backdrop-blur-md shadow-lg dark:shadow-neutral-950/50 rounded-xl overflow-hidden ${className}`}
      {...props}
    >
      {title && (
        <div className={`px-5 py-4 md:px-6 md:py-5 border-b border-neutral-200 dark:border-neutral-700/80 ${titleClassName}`}>
          <h3 className="text-lg md:text-xl font-semibold text-neutral-800 dark:text-neutral-100">{title}</h3>
        </div>
      )}
      <div className={`p-5 md:p-6 ${bodyClassName}`}>
        {children}
      </div>
      {footer && (
        <div className={`px-5 py-4 md:px-6 md:py-4 bg-neutral-50 dark:bg-neutral-800/50 border-t border-neutral-200 dark:border-neutral-700/80 ${footerClassName}`}>
          {footer}
        </div>
      )}
    </div>
  );
};