import React, { useState, useEffect } from 'react';
import { Card } from '../ui/Card';
import { Button } from '../ui/Button';
import { useAppContext } from '../../hooks/useAppContext';
import { useLanguage } from '../../hooks/useLanguage';
import { apiService } from '../../services/api';
import {
  DocumentReportIcon,
  XIcon,
  FolderIcon,
  EyeIcon,
  DownloadIcon
} from '../../constants';



interface ReportFile {
  filename: string;
  path: string;
  size: number;
}

interface ReportBatch {
  batch_id: string;
  created_time: number;
  md_files: ReportFile[];
  html_files: ReportFile[];
  task_info?: any;
  seminars: string[];
  session_count: number;
  status: string;
}

interface ReportFilesResponse {
  reports: ReportBatch[];
}

export const BatchReportTasksPage: React.FC = () => {
  const { setPageTitle } = useAppContext();
  const { t } = useLanguage();

  const [reportBatches, setReportBatches] = useState<ReportBatch[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setPageTitle(t('batchReportTasks', 'sidebar'));
    loadReports();
  }, [setPageTitle, t]);

  const loadReports = async () => {
    setLoading(true);
    setError(null);
    try {
      console.log('正在載入報告文件...');
      const filesResponse = await apiService.getReportFiles();
      console.log('文件響應:', filesResponse);
      setReportBatches(filesResponse.reports || []);
    } catch (error: any) {
      console.error('載入報告文件失敗:', error);
      setError(`載入報告文件失敗: ${error.message || '未知錯誤'}`);
    } finally {
      setLoading(false);
    }
  };



  const formatTimestamp = (timestamp: number): string => {
    return new Date(timestamp * 1000).toLocaleString('zh-TW');
  };

  const handlePreviewFile = (filePath: string) => {
    const encodedPath = encodeURIComponent(filePath);
    const previewUrl = `${apiService.baseURL}/reports/preview/${encodedPath}`;
    window.open(previewUrl, '_blank');
  };

  const handleDownloadFile = async (filePath: string, filename: string) => {
    try {
      await apiService.downloadReportFile(filePath, filename);
    } catch (error: any) {
      console.error('下載文件失敗:', error);
      setError(`下載文件失敗: ${error.message || '未知錯誤'}`);
    }
  };

  const handleDownloadZip = async (batchId: string) => {
    try {
      setError(null);

      // 檢查是否有對應的任務
      const taskId = batchId; // 假設 batch_id 就是 task_id

      // 調用 ZIP 下載 API
      const response = await fetch(`${apiService.baseURL}/batch-reports/${taskId}/download-zip`, {
        method: 'GET',
        headers: {
          'Accept': 'application/zip',
        },
      });

      if (!response.ok) {
        if (response.status === 404) {
          throw new Error('ZIP 文件不存在或任務未完成');
        } else if (response.status === 400) {
          throw new Error('任務尚未完成');
        } else {
          throw new Error(`下載失敗: ${response.statusText}`);
        }
      }

      // 獲取文件名
      const contentDisposition = response.headers.get('Content-Disposition');
      let filename = `TrendScope-會議報告-${batchId}.zip`;
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename=(.+)/);
        if (filenameMatch) {
          filename = filenameMatch[1].replace(/['"]/g, '');
        }
      }

      // 下載文件
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

    } catch (error: any) {
      console.error('下載 ZIP 文件失敗:', error);
      setError(`下載 ZIP 文件失敗: ${error.message || '未知錯誤'}`);
    }
  };





  return (
    <div className="space-y-6">
      {/* 頁面標題 */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <DocumentReportIcon className="w-8 h-8 text-blue-600" />
          <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">
            {t('batchReportTasks', 'sidebar')}
          </h1>
        </div>
        <div className="flex items-center space-x-4">
          <Button
            variant="secondary"
            onClick={loadReports}
            disabled={loading}
          >
            {loading ? '載入中...' : '刷新'}
          </Button>
        </div>
      </div>

      {/* 錯誤提示 */}
      {error && (
        <Card className="border-red-200 bg-red-50 dark:bg-red-900/20">
          <div className="flex items-center space-x-2 text-red-700 dark:text-red-300">
            <XIcon className="w-5 h-5" />
            <span>{error}</span>
          </div>
        </Card>
      )}







      {/* 已生成的報告 */}
      {reportBatches.length > 0 && (
        <div>
          <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">
            已生成的報告
          </h2>
          <div className="space-y-4">
            {reportBatches.map((batch) => (
              <Card key={batch.batch_id}>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <FolderIcon className="w-6 h-6 text-blue-600" />
                      <div>
                        <h3 className="font-semibold text-gray-900 dark:text-gray-100">
                          {batch.batch_id}
                        </h3>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          生成時間: {formatTimestamp(batch.created_time)}
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-4">
                      <div className="flex items-center space-x-2 text-sm text-gray-600 dark:text-gray-400">
                        <span>{batch.md_files.length} MD</span>
                        <span>•</span>
                        <span>{batch.html_files.length} HTML</span>
                      </div>
                      <Button
                        variant="primary"
                        size="sm"
                        onClick={() => handleDownloadZip(batch.batch_id)}
                        leftIcon={<DownloadIcon className="w-4 h-4" />}
                        className="bg-green-600 hover:bg-green-700 text-white"
                      >
                        下載 ZIP
                      </Button>
                    </div>
                  </div>

                  {/* HTML 文件列表 */}
                  {batch.html_files.length > 0 && (
                    <div>
                      <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-2">
                        HTML 報告
                      </h4>
                      <div className="space-y-2">
                        {batch.html_files.map((file, index) => (
                          <div key={index} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                            <div className="flex-1 min-w-0">
                              <p className="text-sm font-medium text-gray-900 dark:text-gray-100 truncate">
                                {file.filename}
                              </p>
                              <p className="text-xs text-gray-500 dark:text-gray-400">
                                {(file.size / 1024).toFixed(1)} KB
                              </p>
                            </div>
                            <div className="flex items-center space-x-2 ml-4">
                              <Button
                                variant="primary"
                                size="sm"
                                onClick={() => handlePreviewFile(file.path)}
                                leftIcon={<EyeIcon className="w-4 h-4" />}
                              >
                                預覽
                              </Button>
                              <Button
                                variant="secondary"
                                size="sm"
                                onClick={() => handleDownloadFile(file.path, file.filename)}
                                leftIcon={<DownloadIcon className="w-4 h-4" />}
                              >
                                下載
                              </Button>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* MD 文件列表 */}
                  {batch.md_files.length > 0 && (
                    <div>
                      <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-2">
                        Markdown 文件
                      </h4>
                      <div className="space-y-2">
                        {batch.md_files.map((file, index) => (
                          <div key={index} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                            <div className="flex-1 min-w-0">
                              <p className="text-sm font-medium text-gray-900 dark:text-gray-100 truncate">
                                {file.filename}
                              </p>
                              <p className="text-xs text-gray-500 dark:text-gray-400">
                                {(file.size / 1024).toFixed(1)} KB
                              </p>
                            </div>
                            <div className="flex items-center space-x-2 ml-4">
                              <Button
                                variant="secondary"
                                size="sm"
                                onClick={() => handleDownloadFile(file.path, file.filename)}
                                leftIcon={<DownloadIcon className="w-4 h-4" />}
                              >
                                下載
                              </Button>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* 空狀態 */}
      {reportBatches.length === 0 && !loading && (
        <Card>
          <div className="text-center py-8">
            <FolderIcon className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-500">沒有找到任何已生成的報告</p>
          </div>
        </Card>
      )}
    </div>
  );
};
