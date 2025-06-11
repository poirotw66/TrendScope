
import React, { useEffect, useState } from 'react';
import { useAppContext } from '../../hooks/useAppContext';
import { useLanguage } from '../../hooks/useLanguage';
import { Card } from '../ui/Card';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';
import { SearchIcon, FilterIcon, DownloadIcon } from '../../constants';

interface LogEntry {
  id: string;
  timestamp: string;
  level: 'INFO' | 'WARN' | 'ERROR' | 'DEBUG';
  message: string;
  source?: string;
}

const mockLogs: LogEntry[] = Array.from({ length: 100 }, (_, i) => ({
  id: `log-${i}`,
  timestamp: new Date(Date.now() - i * 60000 * Math.random() * 10).toISOString(),
  level: (['INFO', 'WARN', 'ERROR', 'DEBUG'] as LogEntry['level'][])[i % 4],
  message: `This is a mock log entry number ${i + 1}. Operation: ${['UserLogin', 'DataFetch', 'SystemUpdate', 'CrawlerRun'][i%4]} ${i%3 === 0 ? 'succeeded' : 'failed with details...'}.`,
  source: `service-${String.fromCharCode(65 + (i % 5))}`,
}));


export const LogQueryPage: React.FC = () => {
  const { setPageTitle, setLoading } = useAppContext();
  const { t } = useLanguage();

  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterLevel, setFilterLevel] = useState('');
  const [filterDate, setFilterDate] = useState(''); // Could be date range picker

  useEffect(() => {
    setPageTitle(t('logQuery', 'sidebar'));
    setLoading(true);
    // Simulate fetching logs
    setTimeout(() => {
      setLogs(mockLogs);
      setLoading(false);
    }, 500);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [setPageTitle, t]);

  const filteredLogs = logs.filter(log => {
    const matchesSearch = log.message.toLowerCase().includes(searchTerm.toLowerCase()) || (log.source && log.source.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesLevel = filterLevel ? log.level === filterLevel : true;
    const matchesDate = filterDate ? log.timestamp.startsWith(filterDate) : true; // Simplified date filter
    return matchesSearch && matchesLevel && matchesDate;
  }).slice(0, 50); // Display max 50 logs for performance with mock data

  const handleDownloadLogs = () => {
    // In a real app, this would trigger a download of filtered logs
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(filteredLogs));
    const downloadAnchorNode = document.createElement('a');
    downloadAnchorNode.setAttribute("href", dataStr);
    downloadAnchorNode.setAttribute("download", "trendscope_logs.json");
    document.body.appendChild(downloadAnchorNode); // required for firefox
    downloadAnchorNode.click();
    downloadAnchorNode.remove();
    alert(t('downloadLogs', 'logs') + ': ' + t('success').toLowerCase());
  };


  return (
    <div className="space-y-6">
      <Card>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <Input
            type="text"
            placeholder={t('searchLogs', 'logs')}
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            icon={<SearchIcon className="w-5 h-5" />}
          />
          <Input
            type="date" // Simplified date filter
            value={filterDate}
            onChange={(e) => setFilterDate(e.target.value)}
            label={t('filterByDate', 'logs')}
          />
          <div className="flex flex-col">
             <label htmlFor="logLevelFilter" className="block text-sm font-medium text-neutral-700 dark:text-neutral-300 mb-1">
              {t('filterByLevel', 'logs')}
            </label>
            <select 
              id="logLevelFilter"
              value={filterLevel} 
              onChange={(e) => setFilterLevel(e.target.value)}
              className="block w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm bg-white dark:bg-neutral-700 text-neutral-900 dark:text-neutral-100"
            >
              <option value="">All Levels</option>
              <option value="INFO">INFO</option>
              <option value="WARN">WARN</option>
              <option value="ERROR">ERROR</option>
              <option value="DEBUG">DEBUG</option>
            </select>
          </div>
        </div>
        <div className="flex justify-end mb-4">
          <Button variant="secondary" onClick={handleDownloadLogs} leftIcon={<DownloadIcon className="w-4 h-4" />}>
            {t('downloadLogs', 'logs')}
          </Button>
        </div>

        <div className="overflow-x-auto max-h-[60vh] bg-neutral-800 dark:bg-black p-4 rounded-md shadow">
          <pre className="text-xs text-neutral-200 dark:text-neutral-300 whitespace-pre-wrap">
            {filteredLogs.length > 0 
             ? filteredLogs.map(log => 
                `${log.timestamp} [${log.level}] ${log.source ? `(${log.source}) ` : ''}${log.message}`
               ).join('\n')
             : t('noData')
            }
          </pre>
        </div>
      </Card>
    </div>
  );
};
