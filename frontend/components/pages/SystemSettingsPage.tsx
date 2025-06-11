
import React, { useEffect, useState } from 'react';
import { useAppContext } from '../../hooks/useAppContext';
import { useLanguage } from '../../hooks/useLanguage';
import { Card } from '../ui/Card';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';

export const SystemSettingsPage: React.FC = () => {
  const { setPageTitle } = useAppContext();
  const { t } = useLanguage();

  const [settings, setSettings] = useState({
    someApiKey: '',
    bigQueryProject: '',
    cloudStorageBucket: '',
    maxUsers: '100',
  });

  useEffect(() => {
    setPageTitle(t('systemSettings', 'sidebar'));
    // In a real app, fetch current settings here
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [setPageTitle, t]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setSettings(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // console.log("Settings saved:", settings);
    // In a real app, save settings to backend
    alert(t('save') + ' ' + t('success').toLowerCase());
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <Card title={t('apiKeys', 'settings')}>
        <p className="text-sm text-neutral-500 dark:text-neutral-400 mb-4">{t('apiKeyNote', 'settings')}</p>
        <Input
          label="Some External API Key"
          id="someApiKey"
          name="someApiKey"
          type="password"
          value={settings.someApiKey}
          onChange={handleChange}
          placeholder="Enter API Key"
        />
      </Card>

      <Card title={t('bigQueryStorage', 'settings')}>
        <div className="space-y-4">
          <Input
            label="BigQuery Project ID"
            id="bigQueryProject"
            name="bigQueryProject"
            value={settings.bigQueryProject}
            onChange={handleChange}
            placeholder="your-gcp-project-id"
          />
          <Input
            label="Cloud Storage Bucket Name"
            id="cloudStorageBucket"
            name="cloudStorageBucket"
            value={settings.cloudStorageBucket}
            onChange={handleChange}
            placeholder="your-storage-bucket-name"
          />
        </div>
      </Card>
      
      <Card title={t('userPermissions', 'settings')}>
        <p className="text-sm text-neutral-500 dark:text-neutral-400">
          {/* Placeholder for user permission management UI. This would typically be a more complex module. */}
          User permission management interface would go here (e.g., roles, user lists, etc.).
        </p>
      </Card>

      <Card title={t('systemParameters', 'settings')}>
         <Input
            label="Max Concurrent Users"
            id="maxUsers"
            name="maxUsers"
            type="number"
            value={settings.maxUsers}
            onChange={handleChange}
          />
      </Card>

      <div className="flex justify-end">
        <Button type="submit" variant="primary">{t('save')} {t('settings')}</Button>
      </div>
    </form>
  );
};
