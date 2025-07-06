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
  const { setPageTitle, addNotification } = useAppContext();
  const { t } = useLanguage();

  const [reportBatches, setReportBatches] = useState<ReportBatch[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [downloadingTasks, setDownloadingTasks] = useState<Record<string, boolean>>({});

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

  // 修復後的下載函數 - 解決 React Hooks 規則問題
  const handleDownloadZip = async (batchId: string) => {
    console.log('🖱️ [DEBUG] 下載函數被調用:', batchId);
    console.log('🔧 [DEBUG] addNotification 可用:', typeof addNotification);

    try {
      setError(null);
      setDownloadingTasks(prev => ({ ...prev, [batchId]: true }));

      console.log('🚀 [DEBUG] 開始下載 ZIP 文件:', batchId);
      console.log('🔧 [DEBUG] API 基礎 URL:', apiService.baseURL);
      console.log('🔧 [DEBUG] 當前時間:', new Date().toISOString());

      // 獲取可用的 ZIP 文件列表
      console.log('📋 [DEBUG] 步驟 1: 獲取 ZIP 文件列表...');
      const listUrl = `${apiService.baseURL}/reports/list-zip-files`;
      console.log('🌐 [DEBUG] 文件列表 URL:', listUrl);

      const listResponse = await fetch(listUrl);
      console.log('📊 [DEBUG] 文件列表響應狀態:', listResponse.status);
      console.log('📋 [DEBUG] 文件列表響應頭:', Object.fromEntries(listResponse.headers.entries()));

      if (!listResponse.ok) {
        const errorText = await listResponse.text();
        console.error('❌ [DEBUG] 文件列表 API 失敗:', errorText);
        throw new Error(`無法獲取 ZIP 文件列表: ${listResponse.status} ${errorText}`);
      }

      const zipFiles = await listResponse.json();
      console.log('📁 [DEBUG] 所有 ZIP 文件:', zipFiles);

      const batchIdClean = batchId.replace('batch_', '');
      console.log('🔍 [DEBUG] 清理後的 batch ID:', batchIdClean);

      const matchingFiles = zipFiles.filter((filename: string) =>
        filename.includes(batchIdClean)
      );

      console.log(`🎯 [DEBUG] 找到 ${matchingFiles.length} 個匹配文件:`, matchingFiles);

      if (matchingFiles.length === 0) {
        console.error('❌ [DEBUG] 沒有找到匹配的文件');
        console.log('🔍 [DEBUG] 搜索條件:', batchIdClean);
        console.log('📁 [DEBUG] 可用文件:', zipFiles);
        throw new Error('找不到對應的 ZIP 文件');
      }

      const targetFile = matchingFiles[0];
      console.log('🎯 [DEBUG] 目標文件:', targetFile);

      const encodedFilename = encodeURIComponent(targetFile);
      console.log('🔤 [DEBUG] 編碼後文件名:', encodedFilename);

      const downloadUrl = `${apiService.baseURL}/reports/download-zip/${encodedFilename}`;
      console.log('🌐 [DEBUG] 下載 URL:', downloadUrl);

      // 方法 1: 直接跳轉下載（最可靠）
      try {
        console.log('📥 [DEBUG] 步驟 2: 方法 1 - 使用 window.location.href');
        console.log('🌐 [DEBUG] 即將跳轉到:', downloadUrl);
        console.log('🕐 [DEBUG] 跳轉時間:', new Date().toISOString());

        // 添加一個小延遲來確保日誌被記錄
        await new Promise(resolve => setTimeout(resolve, 100));

        window.location.href = downloadUrl;

        console.log('✅ [DEBUG] window.location.href 已執行');

        addNotification({
          message: 'ZIP 文件下載已開始！請檢查瀏覽器下載文件夾。',
          type: 'success'
        });

        console.log('✅ [DEBUG] 直接跳轉下載成功');
        return;

      } catch (directError) {
        console.error('❌ [DEBUG] 直接跳轉下載失敗:', directError);
        console.log('🔄 [DEBUG] 嘗試備用方法...');
      }

      // 方法 2: 使用 window.open（備用方法）
      try {
        console.log('📥 方法 2: 使用 window.open');
        const newWindow = window.open(downloadUrl, '_blank');

        if (newWindow) {
          // 短暫延遲後關閉窗口
          setTimeout(() => {
            newWindow.close();
          }, 1000);

          addNotification({
            message: 'ZIP 文件下載已開始！請檢查瀏覽器下載文件夾。',
            type: 'success'
          });

          console.log('✅ window.open 下載成功');
          return;
        }
      } catch (openError) {
        console.warn('window.open 下載失敗，嘗試最後方法:', openError);
      }

      // 方法 3: 創建隱藏的 iframe（最後備用方法）
      try {
        console.log('📥 方法 3: 使用隱藏 iframe');
        const iframe = document.createElement('iframe');
        iframe.style.display = 'none';
        iframe.src = downloadUrl;
        document.body.appendChild(iframe);

        // 延遲移除 iframe
        setTimeout(() => {
          document.body.removeChild(iframe);
        }, 5000);

        addNotification({
          message: 'ZIP 文件下載已開始！請檢查瀏覽器下載文件夾。',
          type: 'success'
        });

        console.log('✅ iframe 下載成功');

      } catch (iframeError) {
        console.error('所有下載方法都失敗:', iframeError);

        // 提供手動下載鏈接
        addNotification({
          message: `自動下載失敗，請點擊此鏈接手動下載：${downloadUrl}`,
          type: 'warning'
        });

        throw new Error('所有自動下載方法都失敗，請手動下載');
      }

    } catch (error: any) {
      console.error('❌ [DEBUG] 下載 ZIP 文件失敗:', error);
      console.log('🔍 [DEBUG] 錯誤詳情:', {
        message: error.message,
        stack: error.stack,
        name: error.name,
        batchId: batchId,
        timestamp: new Date().toISOString()
      });

      setError(`下載 ZIP 文件失敗: ${error.message || '未知錯誤'}`);

      addNotification({
        message: `下載失敗: ${error.message || '未知錯誤'}`,
        type: 'error'
      });
    } finally {
      setDownloadingTasks(prev => ({ ...prev, [batchId]: false }));
      console.log('🏁 [DEBUG] 下載流程結束:', batchId, '時間:', new Date().toISOString());
    }
  };

  // 簡單的測試函數
  const testDownloadFunction = () => {
    console.log('🧪 [TEST] 測試函數被調用');
    console.log('🧪 [TEST] addNotification 類型:', typeof addNotification);

    try {
      addNotification({
        message: '測試通知功能正常！',
        type: 'success'
      });
      console.log('🧪 [TEST] 通知發送成功');
    } catch (error) {
      console.error('🧪 [TEST] 通知發送失敗:', error);
    }
  };

  // 獲取手動下載鏈接
  const getManualDownloadUrl = async (batchId: string): Promise<string | null> => {
    try {
      const listResponse = await fetch(`${apiService.baseURL}/reports/list-zip-files`);
      if (listResponse.ok) {
        const zipFiles = await listResponse.json();
        const matchingFiles = zipFiles.filter((filename: string) =>
          filename.includes(batchId.replace('batch_', ''))
        );

        if (matchingFiles.length > 0) {
          const targetFile = matchingFiles[0];
          const encodedFilename = encodeURIComponent(targetFile);
          return `${apiService.baseURL}/reports/download-zip/${encodedFilename}`;
        }
      }
    } catch (error) {
      console.error('獲取手動下載鏈接失敗:', error);
    }
    return null;
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

          <Button
            variant="primary"
            onClick={testDownloadFunction}
            className="bg-purple-600 hover:bg-purple-700"
          >
            🧪 測試功能
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
                      <div className="flex items-center space-x-2">
                        <Button
                          variant="primary"
                          size="sm"
                          onClick={() => {
                            console.log('🖱️ [DEBUG] 下載按鈕被點擊:', batch.batch_id);
                            console.log('🔧 [DEBUG] 按鈕狀態:', {
                              disabled: downloadingTasks[batch.batch_id],
                              batchId: batch.batch_id,
                              timestamp: new Date().toISOString()
                            });
                            handleDownloadZip(batch.batch_id);
                          }}
                          disabled={downloadingTasks[batch.batch_id]}
                          leftIcon={<DownloadIcon className="w-4 h-4" />}
                          className={`${
                            downloadingTasks[batch.batch_id]
                              ? 'bg-gray-400 cursor-not-allowed'
                              : 'bg-green-600 hover:bg-green-700'
                          } text-white`}
                        >
                          {downloadingTasks[batch.batch_id] ? '下載中...' : '下載 ZIP'}
                        </Button>

                        <button
                          onClick={async () => {
                            const url = await getManualDownloadUrl(batch.batch_id);
                            if (url) {
                              window.open(url, '_blank');
                            } else {
                              addNotification({
                                message: '無法獲取下載鏈接',
                                type: 'error'
                              });
                            }
                          }}
                          className="text-xs text-blue-600 hover:text-blue-800 underline"
                          title="如果自動下載失敗，請點擊此鏈接手動下載"
                        >
                          手動下載
                        </button>
                      </div>
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
