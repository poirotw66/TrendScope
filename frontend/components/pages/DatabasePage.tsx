
import React, { useEffect, useState, useMemo } from 'react';
import { useAppContext } from '../../hooks/useAppContext';
import { useLanguage } from '../../hooks/useLanguage';
import { getMockTrendData } from '../../services/mockDataService';
import { TrendData } from '../../types';
import { Card } from '../ui/Card';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';
import { Modal } from '../ui/Modal';
import { SearchIcon, FilterIcon, SortAscIcon, EyeIcon, ChevronDownIcon } from '../../constants';

const ITEMS_PER_PAGE = 10;

export const DatabasePage: React.FC = () => {
  const { setPageTitle, setLoading } = useAppContext();
  const { t } = useLanguage();
  
  const [data, setData] = useState<TrendData[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedItem, setSelectedItem] = useState<TrendData | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    setPageTitle(t('databaseManagement', 'sidebar'));
    setLoading(true);
    // Simulate API call
    setTimeout(() => {
      setData(getMockTrendData(50));
      setLoading(false);
    }, 500);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [setPageTitle, t]);

  const filteredData = useMemo(() => {
    return data.filter(item =>
      Object.values(item).some(value =>
        String(value).toLowerCase().includes(searchTerm.toLowerCase())
      )
    );
  }, [data, searchTerm]);

  const paginatedData = useMemo(() => {
    const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
    return filteredData.slice(startIndex, startIndex + ITEMS_PER_PAGE);
  }, [filteredData, currentPage]);

  const totalPages = Math.ceil(filteredData.length / ITEMS_PER_PAGE);

  const handleViewDetails = (item: TrendData) => {
    setSelectedItem(item);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedItem(null);
  };

  const tableHeaderKeys = ['conference', 'meeting', 'abstract', 'topic', 'action'];

  return (
    <div className="space-y-6 md:space-y-8">
      <Card>
        <div className="flex flex-col md:flex-row justify-between items-center gap-4 mb-6">
          <Input
            type="text"
            placeholder={t('search') + '...'}
            value={searchTerm}
            onChange={(e) => { setSearchTerm(e.target.value); setCurrentPage(1);}}
            icon={<SearchIcon className="w-5 h-5" />}
            className="max-w-md w-full md:w-auto"
            wrapperClassName="flex-grow md:flex-grow-0"
          />
          <div className="flex space-x-2">
            <Button variant="secondary" size="md" leftIcon={<FilterIcon className="w-4 h-4" />}>{t('filter')}</Button>
            <Button variant="secondary" size="md" leftIcon={<SortAscIcon className="w-4 h-4" />}>{t('sort')}</Button>
          </div>
        </div>

        <div className="overflow-x-auto rounded-lg border border-neutral-200 dark:border-neutral-700/80">
          <table className="min-w-full divide-y divide-neutral-200 dark:divide-neutral-700/80">
            <thead className="bg-neutral-50 dark:bg-neutral-800/60">
              <tr>
                {tableHeaderKeys.map(key => (
                  <th key={key} scope="col" className="px-6 py-3.5 text-left text-xs font-semibold text-neutral-600 dark:text-neutral-300 uppercase tracking-wider">
                    {t(key, key === 'action' ? 'general' : 'database')}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="bg-white dark:bg-neutral-800 divide-y divide-neutral-200 dark:divide-neutral-700/80">
              {paginatedData.map((item) => (
                <tr key={item.id} className="hover:bg-neutral-50/70 dark:hover:bg-neutral-700/50 transition-colors duration-150">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-neutral-900 dark:text-neutral-100">{item.conference}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-600 dark:text-neutral-300">{item.meeting}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-600 dark:text-neutral-300 truncate max-w-xs" title={item.abstract}>
                    {item.abstract.length > 100 ? `${item.abstract.substring(0, 100)}...` : item.abstract}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-600 dark:text-neutral-300">{item.topic}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <Button variant="ghost" size="sm" onClick={() => handleViewDetails(item)} leftIcon={<EyeIcon className="w-4 h-4"/>}>
                      {t('viewDetails')}
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        
        {paginatedData.length === 0 && (
           <p className="text-center py-8 text-neutral-500 dark:text-neutral-400">{t('noData')}</p>
        )}

        {totalPages > 1 && (
          <div className="mt-6 flex flex-col md:flex-row justify-between items-center gap-4">
            <span className="text-sm text-neutral-600 dark:text-neutral-400">
              {t('Page', 'general')} {currentPage} {t('of', 'general')} {totalPages}
            </span>
            <div className="flex space-x-2">
              <Button
                onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
                disabled={currentPage === 1}
                variant="secondary"
                size="sm"
              >
                {t('Previous', 'general')}
              </Button>
              <Button
                onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
                disabled={currentPage === totalPages}
                variant="secondary"
                size="sm"
              >
                {t('Next', 'general')}
              </Button>
            </div>
          </div>
        )}
      </Card>

      {selectedItem && (
        <Modal
          isOpen={isModalOpen}
          onClose={handleCloseModal}
          title={t('trendDataDetails', 'database')}
          size="lg"
        >
          <div className="space-y-3 text-sm text-neutral-700 dark:text-neutral-300">
            <p><strong className="font-medium text-neutral-800 dark:text-neutral-100">{t('conference', 'database')}:</strong> {selectedItem.conference}</p>
            <p><strong className="font-medium text-neutral-800 dark:text-neutral-100">{t('date', 'database')}:</strong> {selectedItem.date}</p> {/* Date is still shown in modal */}
            <p><strong className="font-medium text-neutral-800 dark:text-neutral-100">{t('meeting', 'database')}:</strong> {selectedItem.meeting}</p>
            <p><strong className="font-medium text-neutral-800 dark:text-neutral-100">{t('url', 'database')}:</strong> <a href={selectedItem.url} target="_blank" rel="noopener noreferrer" className="text-primary-600 dark:text-primary-400 hover:underline">{selectedItem.url}</a></p>
            <p><strong className="font-medium text-neutral-800 dark:text-neutral-100">{t('abstract', 'database')}:</strong> {selectedItem.abstract}</p>
            <p><strong className="font-medium text-neutral-800 dark:text-neutral-100">{t('topic', 'database')}:</strong> {selectedItem.topic}</p>
            {selectedItem.other && <p><strong className="font-medium text-neutral-800 dark:text-neutral-100">{t('other', 'database')}:</strong> {selectedItem.other}</p>}
          </div>
           {/* Footer moved to Modal component's footer prop for consistent styling */}
        </Modal>
      )}
    </div>
  );
};
