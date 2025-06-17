
import React, { useEffect, useState, useMemo } from 'react';
import { useAppContext } from '../../hooks/useAppContext';
import { useLanguage } from '../../hooks/useLanguage';
import { getMockTrendData } from '../../services/mockDataService';
import { apiService } from '../../services/api';
import { TrendData } from '../../types';
import { Card } from '../ui/Card';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';
import { Modal } from '../ui/Modal';
import { SearchIcon, FilterIcon, SortAscIcon, EyeIcon, ChevronDownIcon } from '../../constants';

const ITEMS_PER_PAGE = 10;

export const DatabasePage: React.FC = () => {
  const { setPageTitle, setLoading, setError } = useAppContext();
  const { t } = useLanguage();

  const [data, setData] = useState<TrendData[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedItem, setSelectedItem] = useState<TrendData | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [useMockData, setUseMockData] = useState(false);

  useEffect(() => {
    setPageTitle(t('databaseManagement', 'sidebar'));
    loadData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [setPageTitle, t]);

  const loadData = async () => {
    setLoading(true);
    setError(null);

    try {
      if (useMockData) {
        // 使用 mock 資料作為備用
        setData(getMockTrendData(50));
      } else {
        // 嘗試從 BigQuery 獲取真實資料
        const trendData = await apiService.getTrendData();
        setData(trendData);
      }
    } catch (error: any) {
      console.error('載入資料失敗:', error);
      setError(`載入資料失敗: ${error.message || '未知錯誤'}`);

      // 如果 API 失敗，自動切換到 mock 資料
      if (!useMockData) {
        console.log('切換到 mock 資料');
        setUseMockData(true);
        setData(getMockTrendData(50));
        setError('無法連接到資料庫，顯示模擬資料');
      }
    } finally {
      setLoading(false);
    }
  };

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

  const tableHeaderKeys = ['seminar', 'meeting', 'abstract', 'topic', 'action'];

  // 重新整理資料的處理函數
  const handleRefresh = () => {
    loadData();
  };

  // 切換資料來源的處理函數
  const handleToggleDataSource = () => {
    setUseMockData(!useMockData);
    // 切換後重新載入資料
    setTimeout(() => {
      loadData();
    }, 100);
  };

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
            <Button
              variant={useMockData ? "secondary" : "primary"}
              size="md"
              onClick={handleToggleDataSource}
            >
              {useMockData ? '模擬資料' : 'BigQuery'}
            </Button>
            <Button variant="secondary" size="md" onClick={handleRefresh}>重新整理</Button>
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
                <tr key={item.conference_id || item.id} className="hover:bg-neutral-50/70 dark:hover:bg-neutral-700/50 transition-colors duration-150">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-neutral-900 dark:text-neutral-100">
                    {item.seminar || 'Unknown Seminar'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-600 dark:text-neutral-300">
                    {item.meeting || item.name || 'Untitled Session'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-600 dark:text-neutral-300 truncate max-w-xs" title={item.abstract || item.description}>
                    {(() => {
                      const content = item.abstract || item.description || 'No description available';
                      return content.length > 100 ? `${content.substring(0, 100)}...` : content;
                    })()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-600 dark:text-neutral-300">
                    {item.topic || (item.tags && item.tags.length > 0 ? item.tags[0] : 'General')}
                  </td>
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
            <p><strong className="font-medium text-neutral-800 dark:text-neutral-100">{t('seminar', 'database')}:</strong> {selectedItem.seminar || selectedItem.conference}</p>
            <p><strong className="font-medium text-neutral-800 dark:text-neutral-100">ID:</strong> {selectedItem.conference_id || selectedItem.id}</p>
            <p><strong className="font-medium text-neutral-800 dark:text-neutral-100">{t('date', 'database')}:</strong> {selectedItem.date || (selectedItem.created_at ? new Date(selectedItem.created_at).toLocaleDateString() : 'N/A')}</p>
            <p><strong className="font-medium text-neutral-800 dark:text-neutral-100">{t('meeting', 'database')}:</strong> {selectedItem.meeting || selectedItem.name}</p>
            {(selectedItem.url || selectedItem.pdf_url) && (
              <p><strong className="font-medium text-neutral-800 dark:text-neutral-100">{t('url', 'database')}:</strong>
                {selectedItem.url && <a href={selectedItem.url} target="_blank" rel="noopener noreferrer" className="text-primary-600 dark:text-primary-400 hover:underline ml-2">會議連結</a>}
                {selectedItem.pdf_url && <a href={selectedItem.pdf_url} target="_blank" rel="noopener noreferrer" className="text-primary-600 dark:text-primary-400 hover:underline ml-2">PDF 連結</a>}
              </p>
            )}
            <p><strong className="font-medium text-neutral-800 dark:text-neutral-100">{t('abstract', 'database')}:</strong> {selectedItem.abstract || selectedItem.description || 'No description available'}</p>
            <p><strong className="font-medium text-neutral-800 dark:text-neutral-100">{t('topic', 'database')}:</strong> {selectedItem.topic || (selectedItem.tags && selectedItem.tags.length > 0 ? selectedItem.tags.join(', ') : 'General')}</p>
            {selectedItem.other && <p><strong className="font-medium text-neutral-800 dark:text-neutral-100">{t('other', 'database')}:</strong> {selectedItem.other}</p>}
          </div>
           {/* Footer moved to Modal component's footer prop for consistent styling */}
        </Modal>
      )}
    </div>
  );
};
