
import React, { useEffect, useState, useMemo } from 'react';
import { useAppContext } from '../../hooks/useAppContext';
import { useLanguage } from '../../hooks/useLanguage';
import { Card } from '../ui/Card';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';
import { getMockTrendData } from '../../services/mockDataService';
import { TrendData } from '../../types';

interface ReportFormData {
  dataSourceType: string;
  analysisTemplate: string;
  reportTitle: string;
  reportNotes: string;
}

export const ReportGeneratorPage: React.FC = () => {
  const { setPageTitle, setLoading, addNotification } = useAppContext();
  const { t } = useLanguage();

  const [formData, setFormData] = useState<ReportFormData>({
    dataSourceType: '',
    analysisTemplate: '',
    reportTitle: '',
    reportNotes: '',
  });

  const [dataSourceOptions, setDataSourceOptions] = useState<{ value: string; label: string }[]>([]);

  useEffect(() => {
    setPageTitle(t('reportGenerator', 'sidebar'));
    
    // Fetch and process trend data for data source options
    const trendData = getMockTrendData(); // Assuming this gets all necessary data
    const uniqueConferences = Array.from(new Set(trendData.map(item => item.conference)))
      .sort()
      .map(conference => ({ value: conference, label: conference }));
    setDataSourceOptions(uniqueConferences);
    
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [setPageTitle, t]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    // Simulate report generation
    console.log("Generating report with data:", formData);
    setTimeout(() => {
      setLoading(false);
      addNotification({
        message: `${t('Report Title', 'general')}: "${formData.reportTitle}" ${t('success')}fully generated.`,
        type: 'success',
        timestamp: new Date(),
      });
      // Reset form
      setFormData({
        dataSourceType: '',
        analysisTemplate: '',
        reportTitle: '',
        reportNotes: '',
      });
    }, 1500);
  };

  return (
    <div className="space-y-6 md:space-y-8 max-w-3xl mx-auto">
      <form onSubmit={handleSubmit}>
        <Card title={t('title', 'reportGenerator')}>
          <div className="space-y-8 p-2">
            {/* Section 1: Select Data Range (now just Data Source Type) */}
            <section>
              <h3 className="text-lg font-semibold mb-4 text-neutral-800 dark:text-neutral-100 border-b pb-2 dark:border-neutral-700">
                {t('formSectionDataRange', 'reportGenerator')}
              </h3>
              <Input
                as="select"
                label={t('Data Source Type', 'general')}
                name="dataSourceType"
                value={formData.dataSourceType}
                onChange={handleChange}
                placeholder={t('search', 'general') + ' ' + t('Data Source Type', 'general').toLowerCase() + '...'}
                selectOptions={dataSourceOptions.length > 0 ? dataSourceOptions : [{value: '', label: t('loading') + '...' }]}
                required
              />
            </section>

            {/* Section 2: Set Analysis Template */}
            <section>
              <h3 className="text-lg font-semibold mb-4 text-neutral-800 dark:text-neutral-100 border-b pb-2 dark:border-neutral-700">
                {t('formSectionTemplate', 'reportGenerator')}
              </h3>
              <Input
                as="select"
                label={t('Analysis Template', 'general')}
                name="analysisTemplate"
                value={formData.analysisTemplate}
                onChange={handleChange}
                placeholder={t('search', 'general') + ' ' + t('Analysis Template', 'general').toLowerCase() + '...'}
                selectOptions={[
                    { value: 'trend_analysis', label: 'Trend Analysis Template' },
                    { value: 'comparative_study', label: 'Comparative Study Template' },
                    { value: 'market_overview', label: 'Market Overview Template' },
                ]}
                required
              />
            </section>

            {/* Section 3: Define Report Details */}
            <section>
              <h3 className="text-lg font-semibold mb-4 text-neutral-800 dark:text-neutral-100 border-b pb-2 dark:border-neutral-700">
                {t('formSectionDetails', 'reportGenerator')}
              </h3>
              <Input
                label={t('Report Title', 'general')}
                name="reportTitle"
                value={formData.reportTitle}
                onChange={handleChange}
                placeholder={t('Enter report title', 'general')}
                required
              />
              <Input
                as="textarea"
                label={t('Report Notes (optional)', 'general')}
                name="reportNotes"
                value={formData.reportNotes}
                onChange={handleChange}
                className="mt-4 min-h-[100px]"
                placeholder={t('Add any notes here', 'general')}
              />
            </section>
          </div>
          <div className="px-6 py-4 border-t border-neutral-200 dark:border-neutral-700/80 flex justify-end space-x-3 bg-neutral-50 dark:bg-neutral-800/50 rounded-b-xl">
            <Button type="button" variant="secondary" onClick={() => setFormData({dataSourceType: '', analysisTemplate: '', reportTitle: '', reportNotes: ''})}>
              {t('cancel')}
            </Button>
            <Button type="submit" variant="primary">
              {t('generateReport', 'reportGenerator')}
            </Button>
          </div>
        </Card>
      </form>
    </div>
  );
};
