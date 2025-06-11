import React, { InputHTMLAttributes } from 'react';

interface InputProps extends InputHTMLAttributes<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement> {
  label?: string;
  icon?: React.ReactNode;
  error?: string;
  as?: 'input' | 'textarea' | 'select';
  selectOptions?: { value: string | number; label: string }[];
  wrapperClassName?: string;
}

export const Input: React.FC<InputProps> = ({ 
  label, 
  icon, 
  error, 
  id, 
  className = '', 
  as = 'input', 
  selectOptions, 
  wrapperClassName = '',
  ...props 
}) => {
  const baseInputClasses = "block w-full px-3.5 py-2.5 border border-neutral-300 dark:border-neutral-600/80 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-primary-500/60 focus:border-primary-500 sm:text-sm bg-neutral-50 dark:bg-neutral-700/50 text-neutral-900 dark:text-neutral-100 placeholder-neutral-400 dark:placeholder-neutral-500 transition-colors duration-150";
  const iconPadding = icon ? (as === 'textarea' ? "pt-10" : "pl-10") : ""; // Textarea icon padding needs to be on top
  const errorClasses = error ? "border-red-500 dark:border-red-500/70 focus:ring-red-500/60 focus:border-red-500" : "focus:border-primary-500 dark:focus:border-primary-400";

  const inputId = id || props.name;

  const renderInput = () => {
    if (as === 'textarea') {
      return (
        <textarea
          id={inputId}
          className={`${baseInputClasses} ${iconPadding} ${errorClasses} min-h-[80px] ${className}`}
          {...(props as InputHTMLAttributes<HTMLTextAreaElement>)}
        />
      );
    }
    if (as === 'select') {
      return (
         <select
          id={inputId}
          className={`${baseInputClasses} ${iconPadding} ${errorClasses} ${className}`}
          {...(props as InputHTMLAttributes<HTMLSelectElement>)}
        >
          {props.placeholder && <option value="">{props.placeholder}</option>}
          {selectOptions?.map(opt => <option key={opt.value} value={opt.value}>{opt.label}</option>)}
        </select>
      );
    }
    return (
      <input
        id={inputId}
        className={`${baseInputClasses} ${iconPadding} ${errorClasses} ${className}`}
        {...(props as InputHTMLAttributes<HTMLInputElement>)}
      />
    );
  };
  

  return (
    <div className={`w-full ${wrapperClassName}`}>
      {label && (
        <label htmlFor={inputId} className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">
          {label}
        </label>
      )}
      <div className="relative rounded-lg shadow-sm">
        {icon && (
          <div className={`absolute left-0 pl-3 flex items-center pointer-events-none text-neutral-400 dark:text-neutral-500 ${as === 'textarea' ? 'top-3.5' : 'inset-y-0'}`}>
            {icon}
          </div>
        )}
        {renderInput()}
      </div>
      {error && <p className="mt-1.5 text-xs text-red-600 dark:text-red-400">{error}</p>}
    </div>
  );
};