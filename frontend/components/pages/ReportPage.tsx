
import React, { useEffect, useState, useMemo } from 'react';
import { useAppContext } from '../../hooks/useAppContext';
import { useLanguage } from '../../hooks/useLanguage';
import { getMockReports } from '../../services/mockDataService';
import { Report, ReportStatus } from '../../types';
import { Card } from '../ui/Card';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';
import { Modal } from '../ui/Modal';
import { SearchIcon, FilterIcon, SortAscIcon, EyeIcon, DownloadIcon } from '../../constants';

const ITEMS_PER_PAGE = 10;

export const ReportPage: React.FC = () => {
  const { setPageTitle, setLoading } = useAppContext();
  const { t } = useLanguage();

  const [reports, setReports] = useState<Report[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedReport, setSelectedReport] = useState<Report | null>(null);
  const [isDetailModalOpen, setIsDetailModalOpen] = useState(false);
  
  useEffect(() => {
    setPageTitle(t('reportManagement', 'sidebar'));
    setLoading(true);
    setTimeout(() => {
      setReports(getMockReports(30));
      setLoading(false);
    }, 500);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [setPageTitle, t]);

  const filteredReports = useMemo(() => {
    return reports.filter(report =>
      report.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      report.responsiblePerson.toLowerCase().includes(searchTerm.toLowerCase())
    );
  }, [reports, searchTerm]);

  const paginatedReports = useMemo(() => {
    const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
    return filteredReports.slice(startIndex, startIndex + ITEMS_PER_PAGE);
  }, [filteredReports, currentPage]);

  const totalPages = Math.ceil(filteredReports.length / ITEMS_PER_PAGE);

  const handleViewDetails = (report: Report) => {
    setSelectedReport(report);
    setIsDetailModalOpen(true);
  };

  const handleCloseDetailModal = () => {
    setIsDetailModalOpen(false);
    setSelectedReport(null);
  };

  const getStatusClass = (status: ReportStatus) => {
    return status === ReportStatus.PUBLISHED 
      ? 'bg-green-100 text-green-700 dark:bg-green-700/30 dark:text-green-300' 
      : 'bg-amber-100 text-amber-700 dark:bg-amber-700/30 dark:text-amber-300';
  };

  return (
    <div className="space-y-6 md:space-y-8">
      <Card>
        <div className="flex flex-col md:flex-row justify-between items-center gap-4 mb-6">
          <Input
            type="text"
            placeholder={t('search') + ' ' + t('reportTitle', 'reports') + ', ' + t('responsible', 'reports') + '...'}
            value={searchTerm}
            onChange={(e) => { setSearchTerm(e.target.value); setCurrentPage(1); }}
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
                {['reportTitle', 'date', 'responsible', 'status', 'action'].map(key => (
                  <th key={key} scope="col" className="px-6 py-3.5 text-left text-xs font-semibold text-neutral-600 dark:text-neutral-300 uppercase tracking-wider">
                    {t(key, key === 'action' ? 'general' : 'reports')}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="bg-white dark:bg-neutral-800 divide-y divide-neutral-200 dark:divide-neutral-700/80">
              {paginatedReports.map((report) => (
                <tr key={report.id} className="hover:bg-neutral-50/70 dark:hover:bg-neutral-700/50 transition-colors duration-150">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-neutral-900 dark:text-neutral-100">{report.title}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-600 dark:text-neutral-300">{report.date}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-600 dark:text-neutral-300">{report.responsiblePerson}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    <span className={`px-2.5 py-0.5 inline-flex text-xs leading-5 font-semibold rounded-full ${getStatusClass(report.status)}`}>
                      {t(report.status, 'reports')}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <Button variant="ghost" size="sm" onClick={() => handleViewDetails(report)} leftIcon={<EyeIcon className="w-4 h-4" />}>
                      {t('viewDetails')}
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
         {paginatedReports.length === 0 && (
           <p className="text-center py-8 text-neutral-500 dark:text-neutral-400">{t('noData')}</p>
        )}
        {totalPages > 1 && (
          <div className="mt-6 flex flex-col md:flex-row justify-between items-center gap-4">
            <span className="text-sm text-neutral-600 dark:text-neutral-400">{t('Page', 'general')} {currentPage} {t('of', 'general')} {totalPages}</span>
            <div className="flex space-x-2">
              <Button onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))} disabled={currentPage === 1} variant="secondary" size="sm">{t('Previous', 'general')}</Button>
              <Button onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))} disabled={currentPage === totalPages} variant="secondary" size="sm">{t('Next', 'general')}</Button>
            </div>
          </div>
        )}
      </Card>

      {selectedReport && (
        <Modal
          isOpen={isDetailModalOpen}
          onClose={handleCloseDetailModal}
          title={t('reportDetails', 'reports')}
          size="xl"
          footer={
             <div className="flex flex-col sm:flex-row w-full justify-between sm:justify-end items-center gap-3">
                <div className="flex space-x-3">
                    <Button variant="secondary" size="md" leftIcon={<DownloadIcon className="w-4 h-4" />}>{t('downloadPdf', 'reports')}</Button>
                    <Button variant="secondary" size="md" leftIcon={<DownloadIcon className="w-4 h-4" />}>{t('downloadJson', 'reports')}</Button>
                </div>
                <Button onClick={handleCloseDetailModal} size="md">{t('close')}</Button>
            </div>
          }
        >
          <div className="space-y-4 text-sm text-neutral-700 dark:text-neutral-300">
            <p><strong className="font-medium text-neutral-800 dark:text-neutral-100">{t('reportTitle', 'reports')}:</strong> {selectedReport.title}</p>
            <p><strong className="font-medium text-neutral-800 dark:text-neutral-100">{t('date', 'reports')}:</strong> {selectedReport.date}</p>
            <p><strong className="font-medium text-neutral-800 dark:text-neutral-100">{t('responsible', 'reports')}:</strong> {selectedReport.responsiblePerson}</p>
            <p><strong className="font-medium text-neutral-800 dark:text-neutral-100">{t('status', 'reports')}:</strong> <span className={`px-2 py-0.5 text-xs font-semibold rounded-full ${getStatusClass(selectedReport.status)}`}>{t(selectedReport.status, 'reports')}</span></p>
            <div className="pt-2">
              <h4 className="font-semibold text-neutral-800 dark:text-neutral-100 mb-2">{t('dataSources', 'reports')}:</h4>
              <p className="text-xs italic bg-neutral-50 dark:bg-neutral-700/50 p-3 rounded-md">Mock data source summary content. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
            </div>
            <div className="pt-2">
              <h4 className="font-semibold text-neutral-800 dark:text-neutral-100 mb-2">{t('analysisCharts', 'reports')}:</h4>
              <div className="h-40 bg-neutral-100 dark:bg-neutral-700/50 rounded-lg flex items-center justify-center text-neutral-400 dark:text-neutral-500 text-sm">
                {t('Mock Chart Area', 'general')}
              </div>
            </div>
          </div>
        </Modal>
      )}
    </div>
  );
};
