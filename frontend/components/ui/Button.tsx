import React, { ButtonHTMLAttributes } from 'react';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost' | 'link';
  size?: 'sm' | 'md' | 'lg' | 'icon';
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  isLoading?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  leftIcon,
  rightIcon,
  isLoading = false,
  className = '',
  ...props
}) => {
  const baseStyles = 'inline-flex items-center justify-center font-medium rounded-lg focus:outline-none focus:ring-4 focus:ring-opacity-30 transition-all duration-150 disabled:opacity-60 disabled:cursor-not-allowed whitespace-nowrap';

  const variantStyles = {
    primary: 'bg-primary-500 text-white hover:bg-primary-600 focus:ring-primary-500/50 shadow-sm hover:shadow-md active:bg-primary-700',
    secondary: 'bg-neutral-100 text-neutral-700 hover:bg-neutral-200 dark:bg-neutral-700 dark:text-neutral-200 dark:hover:bg-neutral-600 focus:ring-primary-500/50 border border-neutral-300 dark:border-neutral-600 dark:hover:border-neutral-500',
    danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500/50 shadow-sm hover:shadow-md',
    ghost: 'text-neutral-600 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-700/60 focus:ring-primary-500/50 hover:text-primary-600 dark:hover:text-primary-400',
    link: 'text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 hover:underline focus:ring-primary-500/50 underline-offset-2',
  };

  const sizeStyles = {
    sm: `px-3.5 py-2 text-sm ${leftIcon || rightIcon ? 'space-x-1.5' : ''}`,
    md: `px-5 py-2.5 text-sm ${leftIcon || rightIcon ? 'space-x-2' : ''}`,
    lg: `px-6 py-3 text-base ${leftIcon || rightIcon ? 'space-x-2' : ''}`,
    icon: 'p-2.5',
  };
  
  const iconSizeClass = size === 'sm' ? 'w-4 h-4' : size === 'lg' ? 'w-6 h-6' : 'w-5 h-5';


  return (
    <button
      type="button"
      className={`${baseStyles} ${variantStyles[variant]} ${sizeStyles[size]} ${className}`}
      disabled={isLoading || props.disabled}
      {...props}
    >
      {isLoading && (
        <svg className={`animate-spin ${leftIcon ? '-ml-0.5 mr-2' : 'mr-2'} ${iconSizeClass} ${variant ==='primary' || variant === 'danger' ? 'text-white': ''}`} xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      )}
      {leftIcon && !isLoading && <span className={`${iconSizeClass}`}>{leftIcon}</span>}
      {size !== 'icon' && children}
      {rightIcon && !isLoading &&  <span className={`${iconSizeClass}`}>{rightIcon}</span>}
    </button>
  );
};