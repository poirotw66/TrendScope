
import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAppContext } from '../../hooks/useAppContext';
import { useLanguage } from '../../hooks/useLanguage';
import { Button } from '../ui/Button';
import { HomeIcon } from '../../constants';

export const NotFoundPage: React.FC = () => {
  const { setPageTitle } = useAppContext();
  const { t } = useLanguage();

  useEffect(() => {
    setPageTitle('404 - Page Not Found');
     // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [setPageTitle]);

  return (
    <div className="flex flex-col items-center justify-center h-full text-center">
      <h1 className="text-6xl font-bold text-primary-600 dark:text-primary-400">404</h1>
      <p className="mt-4 text-2xl font-medium text-neutral-700 dark:text-neutral-200">
        {t('Oops! Page not found.', 'general')}
      </p>
      <p className="mt-2 text-neutral-500 dark:text-neutral-400">
        {t("The page you are looking for doesn't exist or has been moved.", 'general')}
      </p>
      <Link to="/" className="mt-8">
        <Button variant="primary" leftIcon={<HomeIcon className="w-5 h-5" />}>
          {t('Go to Dashboard', 'general')}
        </Button>
      </Link>
    </div>
  );
};
