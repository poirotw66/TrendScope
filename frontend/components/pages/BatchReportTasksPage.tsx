import React, { useState, useEffect } from 'react';
import { Card } from '../ui/Card';
import { Button } from '../ui/Button';
import { useAppContext } from '../../hooks/useAppContext';
import { useLanguage } from '../../hooks/useLanguage';
import { apiService } from '../../services/api';
import {
  DocumentReportIcon,
  ClockIcon,
  CheckIcon,
  XIcon,
  PlayIcon,
  FolderIcon,
  EyeIcon,
  DownloadIcon
} from '../../constants';

interface BatchReportTask {
  task_id: string;
  type: string;
  status: string;
  seminars: string[];
  estimated_sessions: number;
  start_time: string;
  end_time?: string;
  error_message?: string;
  progress: {
    current: number;
    total: number;
    current_session: string;
  };
  results?: {
    processed_sessions: number;
    failed_sessions: number;
    output_directory: string;
    md_directory: string;
    html_directory?: string;
  };
}

interface BatchReportTasksResponse {
  tasks: Record<string, BatchReportTask>;
}

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
  
  const [tasks, setTasks] = useState<Record<string, BatchReportTask>>({});
  const [reportBatches, setReportBatches] = useState<ReportBatch[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [autoRefresh, setAutoRefresh] = useState(true);

  useEffect(() => {
    setPageTitle(t('batchReportTasks', 'sidebar'));
    loadTasks();
  }, [setPageTitle, t]);

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (autoRefresh) {
      interval = setInterval(loadTasks, 3000); // 每3秒刷新一次
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [autoRefresh]);

  const loadTasks = async () => {
    if (!loading) {
      setLoading(true);
    }
    setError(null);
    try {
      console.log('開始載入數據...');

      // 先只測試報告文件 API
      console.log('正在調用 getReportFiles...');
      const filesResponse = await apiService.getReportFiles();
      console.log('文件響應:', filesResponse);

      setReportBatches(filesResponse.reports || []);

      // 然後測試任務列表 API
      console.log('正在調用 listBatchReportTasks...');
      const tasksResponse = await apiService.listBatchReportTasks();
      console.log('任務響應:', tasksResponse);

      setTasks(tasksResponse.tasks || {});
    } catch (error: any) {
      console.error('載入數據失敗:', error);
      console.error('錯誤詳情:', error.stack);
      setError(`載入數據失敗: ${error.message || '未知錯誤'}`);
    } finally {
      setLoading(false);
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckIcon className="w-5 h-5 text-green-500" />;
      case 'failed':
        return <XIcon className="w-5 h-5 text-red-500" />;
      case 'running':
        return <ClockIcon className="w-5 h-5 text-blue-500 animate-spin" />;
      case 'pending':
        return <ClockIcon className="w-5 h-5 text-yellow-500" />;
      default:
        return <ClockIcon className="w-5 h-5 text-gray-500" />;
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'pending': return '等待中';
      case 'running': return '執行中';
      case 'completed': return '已完成';
      case 'failed': return '失敗';
      default: return '未知';
    }
  };

  const formatDate = (dateString: string): string => {
    return new Date(dateString).toLocaleString('zh-TW');
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

  const testApiConnection = async () => {
    try {
      console.log('測試 API 連接...');
      console.log('API baseURL:', apiService.baseURL);

      // 測試基本連接
      const response = await fetch('http://localhost:8001/');
      const data = await response.json();
      console.log('基本連接測試成功:', data);

      // 測試報告文件 API
      const filesResponse = await fetch('http://localhost:8001/reports/files');
      const filesData = await filesResponse.json();
      console.log('報告文件 API 測試成功:', filesData);

      setError(null);
    } catch (error: any) {
      console.error('API 連接測試失敗:', error);
      setError(`API 連接測試失敗: ${error.message}`);
    }
  };

  const taskList = Object.values(tasks).sort((a, b) => 
    new Date(b.start_time).getTime() - new Date(a.start_time).getTime()
  );

  const runningTasks = taskList.filter(task => task.status === 'running' || task.status === 'pending');
  const completedTasks = taskList.filter(task => task.status === 'completed' || task.status === 'failed');

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
          <div className="flex items-center space-x-2">
            <input
              type="checkbox"
              id="autoRefresh"
              checked={autoRefresh}
              onChange={(e) => setAutoRefresh(e.target.checked)}
              className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            <label htmlFor="autoRefresh" className="text-sm text-gray-700 dark:text-gray-300">
              自動刷新
            </label>
          </div>
          <Button
            variant="secondary"
            onClick={loadTasks}
            disabled={loading}
            leftIcon={loading ? <ClockIcon className="w-4 h-4 animate-spin" /> : undefined}
          >
            {loading ? '載入中...' : '手動刷新'}
          </Button>
          <Button
            variant="outline"
            onClick={testApiConnection}
          >
            測試 API 連接
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

      {/* 統計信息 */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card>
          <div className="flex items-center space-x-3">
            <PlayIcon className="w-8 h-8 text-blue-500" />
            <div>
              <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                {runningTasks.length}
              </p>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                正在執行的任務
              </p>
            </div>
          </div>
        </Card>
        
        <Card>
          <div className="flex items-center space-x-3">
            <CheckIcon className="w-8 h-8 text-green-500" />
            <div>
              <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                {completedTasks.filter(t => t.status === 'completed').length}
              </p>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                已完成的任務
              </p>
            </div>
          </div>
        </Card>
        
        <Card>
          <div className="flex items-center space-x-3">
            <XIcon className="w-8 h-8 text-red-500" />
            <div>
              <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                {completedTasks.filter(t => t.status === 'failed').length}
              </p>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                失敗的任務
              </p>
            </div>
          </div>
        </Card>
      </div>

      {/* 正在執行的任務 */}
      {runningTasks.length > 0 && (
        <div>
          <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">
            正在執行的任務
          </h2>
          <div className="space-y-4">
            {runningTasks.map((task) => (
              <Card key={task.task_id}>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      {getStatusIcon(task.status)}
                      <div>
                        <h3 className="font-semibold text-gray-900 dark:text-gray-100">
                          任務 ID: {task.task_id.slice(0, 8)}...
                        </h3>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          開始時間: {formatDate(task.start_time)}
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <span className="text-sm font-medium">
                        {getStatusText(task.status)}
                      </span>
                      <p className="text-xs text-gray-500">
                        研討會: {task.seminars.join(', ')}
                      </p>
                    </div>
                  </div>

                  {task.progress && (
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span>進度: {task.progress.current} / {task.progress.total}</span>
                        <span>
                          {task.progress.total > 0
                            ? `${Math.round((task.progress.current / task.progress.total) * 100)}%`
                            : '0%'
                          }
                        </span>
                      </div>
                      <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                        <div
                          className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                          style={{
                            width: task.progress.total > 0
                              ? `${(task.progress.current / task.progress.total) * 100}%`
                              : '0%'
                          }}
                        />
                      </div>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        {task.progress.current_session}
                      </p>
                    </div>
                  )}
                </div>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* 歷史任務 */}
      {completedTasks.length > 0 && (
        <div>
          <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">
            歷史任務
          </h2>
          <div className="space-y-4">
            {completedTasks.map((task) => (
              <Card key={task.task_id}>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      {getStatusIcon(task.status)}
                      <div>
                        <h3 className="font-semibold text-gray-900 dark:text-gray-100">
                          任務 ID: {task.task_id.slice(0, 8)}...
                        </h3>
                        <div className="text-sm text-gray-600 dark:text-gray-400">
                          <p>開始時間: {formatDate(task.start_time)}</p>
                          {task.end_time && (
                            <p>結束時間: {formatDate(task.end_time)}</p>
                          )}
                        </div>
                      </div>
                    </div>
                    <div className="text-right">
                      <span className="text-sm font-medium">
                        {getStatusText(task.status)}
                      </span>
                      <p className="text-xs text-gray-500">
                        研討會: {task.seminars.join(', ')}
                      </p>
                    </div>
                  </div>

                  {task.results && (
                    <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                      <h4 className="font-medium text-gray-900 dark:text-gray-100 mb-2">
                        執行結果
                      </h4>
                      <div className="grid grid-cols-2 gap-4 text-sm">
                        <div>
                          <span className="text-gray-600 dark:text-gray-400">成功處理:</span>
                          <span className="ml-2 font-medium text-green-600">
                            {task.results.processed_sessions}
                          </span>
                        </div>
                        <div>
                          <span className="text-gray-600 dark:text-gray-400">處理失敗:</span>
                          <span className="ml-2 font-medium text-red-600">
                            {task.results.failed_sessions}
                          </span>
                        </div>
                      </div>
                      <div className="mt-2 text-sm">
                        <span className="text-gray-600 dark:text-gray-400">輸出目錄:</span>
                        <span className="ml-2 font-mono text-xs bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded">
                          {task.results.output_directory}
                        </span>
                      </div>
                    </div>
                  )}

                  {task.error_message && (
                    <div className="p-4 bg-red-50 dark:bg-red-900/20 rounded-lg">
                      <h4 className="font-medium text-red-700 dark:text-red-300 mb-2">
                        錯誤信息
                      </h4>
                      <p className="text-sm text-red-600 dark:text-red-400">
                        {task.error_message}
                      </p>
                    </div>
                  )}
                </div>
              </Card>
            ))}
          </div>
        </div>
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
                    <div className="flex items-center space-x-2 text-sm text-gray-600 dark:text-gray-400">
                      <span>{batch.md_files.length} MD</span>
                      <span>•</span>
                      <span>{batch.html_files.length} HTML</span>
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
      {taskList.length === 0 && reportBatches.length === 0 && !loading && (
        <Card>
          <div className="text-center py-8">
            <FolderIcon className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-500">沒有找到任何報告處理任務或已生成的報告</p>
          </div>
        </Card>
      )}
    </div>
  );
};
