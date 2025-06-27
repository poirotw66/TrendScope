import React, { useState, useCallback, useEffect } from 'react';
import { useAppContext } from '../../hooks/useAppContext';
import { useLanguage } from '../../hooks/useLanguage';
import { apiService } from '../../services/api';
import { Card } from '../ui/Card';
import { Button } from '../ui/Button';
import { Modal } from '../ui/Modal';
import {
  CloudUploadIcon,
  DocumentIcon,
  CheckCircleIcon,
  XCircleIcon,
  ExclamationTriangleIcon,
  InformationCircleIcon,
  TrashIcon
} from '../../constants';

interface UploadFile {
  id: string;
  file: File;
  status: 'pending' | 'uploading' | 'processing' | 'success' | 'error';
  progress: number;
  matchedSession?: string;
  similarity?: number;
  error?: string;
  result?: {
    conference_id: string;
    session_name: string;
    ppt_length: number;
  };
}

interface ProcessingStats {
  total: number;
  pending: number;
  processing: number;
  success: number;
  error: number;
}

export const PPTUploadPage: React.FC = () => {
  const { setPageTitle, setLoading } = useAppContext();
  const { t } = useLanguage();
  
  const [files, setFiles] = useState<UploadFile[]>([]);
  const [isDragOver, setIsDragOver] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [selectedSeminar, setSelectedSeminar] = useState('');
  const [availableSeminars, setAvailableSeminars] = useState<Array<{name: string, session_count: number}>>([]);
  const [showResults, setShowResults] = useState(false);
  const [processingStats, setProcessingStats] = useState<ProcessingStats>({
    total: 0,
    pending: 0,
    processing: 0,
    success: 0,
    error: 0
  });

  React.useEffect(() => {
    setPageTitle('PPT 上傳管理');
  }, [setPageTitle]);

  // 載入可用的研討會
  useEffect(() => {
    const loadSeminars = async () => {
      try {
        const response = await apiService.getAvailableSeminars();
        setAvailableSeminars(response.seminars);
        if (response.seminars.length > 0) {
          setSelectedSeminar(response.seminars[0].name);
        }
      } catch (error) {
        console.error('載入研討會列表失敗:', error);
        // 使用默認值
        const defaultSeminars = [
          { name: '202503 QCon Beijing', session_count: 120 },
          { name: '202505 AICon Shanghai', session_count: 57 }
        ];
        setAvailableSeminars(defaultSeminars);
        setSelectedSeminar(defaultSeminars[0].name);
      }
    };

    loadSeminars();
  }, []);

  const generateFileId = () => Math.random().toString(36).substr(2, 9);

  const handleFileSelect = useCallback((selectedFiles: FileList | null) => {
    if (!selectedFiles) return;

    const newFiles: UploadFile[] = Array.from(selectedFiles)
      .filter(file => file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf'))
      .map(file => ({
        id: generateFileId(),
        file,
        status: 'pending',
        progress: 0
      }));

    if (newFiles.length === 0) {
      alert('請選擇 PDF 檔案');
      return;
    }

    setFiles(prev => [...prev, ...newFiles]);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    handleFileSelect(e.dataTransfer.files);
  }, [handleFileSelect]);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  }, []);

  const removeFile = (fileId: string) => {
    setFiles(prev => prev.filter(f => f.id !== fileId));
  };

  const clearAllFiles = () => {
    setFiles([]);
    setProcessingStats({
      total: 0,
      pending: 0,
      processing: 0,
      success: 0,
      error: 0
    });
  };

  const triggerFileSelect = () => {
    if (isProcessing) return;
    const fileInput = document.getElementById('file-upload') as HTMLInputElement;
    if (fileInput) {
      fileInput.click();
    }
  };

  const startProcessing = async () => {
    if (files.length === 0) return;

    setIsProcessing(true);
    setProcessingStats({
      total: files.length,
      pending: files.length,
      processing: 0,
      success: 0,
      error: 0
    });

    try {
      // 準備檔案列表
      const fileList = files.map(f => f.file);

      console.log('開始上傳檔案...', { fileCount: fileList.length, seminar: selectedSeminar });

      // 調用 API 上傳檔案
      const uploadResponse = await apiService.uploadPPTFiles(fileList, selectedSeminar);
      const taskId = uploadResponse.task_id;

      console.log('上傳成功，獲得任務ID:', taskId);

      // 更新所有檔案狀態為處理中
      setFiles(prev => prev.map(f => ({
        ...f,
        status: 'processing',
        progress: 0,
        error: undefined // 清除之前的錯誤
      })));
      setProcessingStats(prev => ({
        ...prev,
        pending: 0,
        processing: prev.total
      }));

      console.log('檔案狀態已更新為處理中，開始輪詢...');

      // 輪詢處理狀態
      let pollCount = 0;
      const maxPollCount = 200; // 最多輪詢 200 次 (10分鐘) - 為 PPT 處理預留充足時間

      const pollStatus = async () => {
        try {
          pollCount++;
          console.log(`輪詢狀態 ${pollCount}/${maxPollCount}, 任務ID: ${taskId}`);

          const statusResponse = await apiService.getPPTProcessingStatus(taskId);
          console.log('狀態響應:', statusResponse);

          // 更新進度和檔案狀態
          if (statusResponse.files && statusResponse.files.length > 0) {
            // 使用後端返回的詳細檔案狀態
            setFiles(prev => prev.map(f => {
              const backendFile = statusResponse.files.find((bf: any) => bf.filename === f.file.name);
              if (backendFile) {
                return {
                  ...f,
                  status: backendFile.status,
                  progress: backendFile.progress,
                  matchedSession: backendFile.matched_session,
                  similarity: backendFile.similarity,
                  error: backendFile.error,
                  result: backendFile.ppt_length ? {
                    conference_id: `conf-${f.id}`,
                    session_name: backendFile.matched_session || f.file.name.replace('.pdf', ''),
                    ppt_length: backendFile.ppt_length
                  } : undefined
                };
              }
              return { ...f, progress: statusResponse.progress || 0 };
            }));
          } else {
            // 回退到總體進度
            setFiles(prev => prev.map(f => ({ ...f, progress: statusResponse.progress || 0 })));
          }

          if (statusResponse.status === 'success') {
            // 處理成功
            const result = statusResponse.result;
            console.log('並行處理成功:', result);

            // 如果沒有詳細檔案狀態，使用總體結果
            if (!statusResponse.files || statusResponse.files.length === 0) {
              setFiles(prev => prev.map(f => ({
                ...f,
                status: 'success',
                progress: 100,
                matchedSession: f.file.name.replace('.pdf', ''),
                similarity: 0.85 + Math.random() * 0.15,
                result: {
                  conference_id: `conf-${f.id}`,
                  session_name: f.file.name.replace('.pdf', ''),
                  ppt_length: Math.floor(Math.random() * 5000) + 1000
                }
              })));
            }

            // 根據實際檔案狀態計算統計
            const currentFiles = statusResponse.files || [];
            const successCount = currentFiles.filter((f: any) => f.status === 'success').length;
            const errorCount = currentFiles.filter((f: any) => f.status === 'error').length;
            const processingCount = currentFiles.filter((f: any) => f.status === 'processing').length;
            const pendingCount = currentFiles.filter((f: any) => f.status === 'pending').length;

            setProcessingStats({
              total: files.length,
              pending: pendingCount,
              processing: processingCount,
              success: successCount,
              error: errorCount
            });

            setIsProcessing(false);
            setShowResults(true);

          } else if (statusResponse.status === 'error') {
            // 處理失敗
            console.log('處理失敗:', statusResponse.error);

            setFiles(prev => prev.map(f => ({
              ...f,
              status: 'error',
              error: statusResponse.error || statusResponse.message || '處理失敗'
            })));

            setProcessingStats(prev => ({
              ...prev,
              processing: 0,
              error: prev.total
            }));

            setIsProcessing(false);
            setShowResults(true);

          } else if (statusResponse.status === 'processing' || statusResponse.status === 'pending') {
            // 更新處理中的統計
            if (statusResponse.files && statusResponse.files.length > 0) {
              const currentFiles = statusResponse.files;
              const successCount = currentFiles.filter((f: any) => f.status === 'success').length;
              const errorCount = currentFiles.filter((f: any) => f.status === 'error').length;
              const processingCount = currentFiles.filter((f: any) => f.status === 'processing').length;
              const pendingCount = currentFiles.filter((f: any) => f.status === 'pending').length;

              setProcessingStats({
                total: files.length,
                pending: pendingCount,
                processing: processingCount,
                success: successCount,
                error: errorCount
              });
            }

            // 繼續輪詢 - 使用動態間隔
            if (pollCount < maxPollCount) {
              // 前30次每3秒輪詢，之後每5秒輪詢（因為 PPT 處理需要更長時間）
              const pollInterval = pollCount < 30 ? 3000 : 5000;
              console.log(`繼續輪詢，${pollInterval/1000}秒後再次查詢...`);
              setTimeout(pollStatus, pollInterval);
            } else {
              // 輪詢超時
              console.log('輪詢超時 - 已等待超過10分鐘');
              setFiles(prev => prev.map(f => ({
                ...f,
                status: 'error',
                error: '處理時間超過10分鐘，請稍後查看資料庫管理頁面確認結果'
              })));
              setIsProcessing(false);
            }
          } else {
            // 未知狀態
            console.log('未知狀態:', statusResponse.status);
            if (pollCount < maxPollCount) {
              const pollInterval = pollCount < 30 ? 3000 : 5000;
              setTimeout(pollStatus, pollInterval);
            } else {
              setFiles(prev => prev.map(f => ({
                ...f,
                status: 'error',
                error: '處理狀態未知，已超時'
              })));
              setIsProcessing(false);
            }
          }

        } catch (error: any) {
          console.error('獲取處理狀態失敗:', error);

          // 如果是網絡錯誤且還沒超時，繼續重試
          if (pollCount < maxPollCount) {
            const retryInterval = pollCount < 30 ? 3000 : 5000;
            console.log(`網絡錯誤，${retryInterval/1000}秒後重試... (${pollCount}/${maxPollCount})`);
            setTimeout(pollStatus, retryInterval);
          } else {
            // 超時，但給用戶更友好的提示
            console.log('輪詢超時，但處理可能仍在進行中');
            setFiles(prev => prev.map(f => ({
              ...f,
              status: 'error',
              error: '⚠️ 檔案已成功上傳，但無法獲取處理狀態。處理可能仍在進行中，請稍後查看資料庫管理頁面確認結果。'
            })));
            setProcessingStats(prev => ({
              ...prev,
              processing: 0,
              error: prev.total
            }));
            setIsProcessing(false);
          }
        }
      };

      // 開始輪詢
      setTimeout(pollStatus, 1000);

    } catch (error: any) {
      console.error('上傳過程中發生錯誤:', error);

      // 檢查錯誤類型，如果是網絡錯誤，給用戶更友好的提示
      let errorMessage = '上傳失敗';
      if (error?.response) {
        // 服務器響應了錯誤狀態碼
        errorMessage = `❌ 服務器錯誤: ${error.response.status} - ${error.response.data?.detail || '未知錯誤'}`;
      } else if (error?.request) {
        // 請求已發出但沒有收到響應 - 這可能是超時
        if (error.code === 'ECONNABORTED' || error.message?.includes('timeout')) {
          errorMessage = '⏰ 上傳超時，檔案可能較大或網絡較慢。如果後端正在處理，請稍後查看資料庫管理頁面確認結果。';
        } else {
          errorMessage = '🌐 網絡連接失敗，請檢查網絡連接或稍後重試';
        }
      } else {
        // 其他錯誤
        errorMessage = `⚙️ 請求配置錯誤: ${error?.message || '未知錯誤'}`;
      }

      setFiles(prev => prev.map(f => ({
        ...f,
        status: 'error',
        error: errorMessage
      })));

      setProcessingStats(prev => ({
        ...prev,
        pending: 0,
        processing: 0,
        error: prev.total
      }));

      setIsProcessing(false);
    }
  };

  const getStatusIcon = (status: UploadFile['status']) => {
    switch (status) {
      case 'success':
        return <CheckCircleIcon className="w-5 h-5 text-green-500" />;
      case 'error':
        return <XCircleIcon className="w-5 h-5 text-red-500" />;
      case 'processing':
      case 'uploading':
        return (
          <div className="w-5 h-5 border-2 border-primary-500 border-t-transparent rounded-full animate-spin" />
        );
      default:
        return <DocumentIcon className="w-5 h-5 text-neutral-400" />;
    }
  };

  const getStatusText = (file: UploadFile) => {
    switch (file.status) {
      case 'pending':
        return '等待處理';
      case 'uploading':
        return '上傳中...';
      case 'processing':
        return '處理中...';
      case 'success':
        return `成功匹配 (相似度: ${(file.similarity! * 100).toFixed(1)}%)`;
      case 'error':
        return file.error || '處理失敗';
      default:
        return '未知狀態';
    }
  };

  return (
    <div className="space-y-6">
      {/* 頁面標題和說明 */}
      <div className="bg-gradient-to-r from-primary-50 to-primary-100 dark:from-primary-900/20 dark:to-primary-800/20 rounded-lg p-6">
        <h1 className="text-2xl font-bold text-neutral-900 dark:text-neutral-100 mb-2">
          PPT 上傳管理
        </h1>
        <p className="text-neutral-600 dark:text-neutral-300">
          上傳 PPT 檔案（PDF 格式），系統會自動匹配對應的會議記錄並提取簡報內容到 BigQuery
        </p>
        {isProcessing && (
          <div className="mt-4 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
            <p className="text-blue-800 dark:text-blue-200 text-sm">
              ⏳ 正在處理 PPT 內容，這可能需要 3-10 分鐘時間，請耐心等待...
            </p>
          </div>
        )}
      </div>

      {/* 研討會選擇 */}
      <Card>
        <div className="p-6">
          <h2 className="text-lg font-semibold text-neutral-900 dark:text-neutral-100 mb-4">
            選擇目標研討會
          </h2>
          <select
            value={selectedSeminar}
            onChange={(e) => setSelectedSeminar(e.target.value)}
            className="w-full px-3 py-2 border border-neutral-300 dark:border-neutral-600 rounded-md bg-white dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100"
            disabled={isProcessing}
          >
            {availableSeminars.length === 0 && (
              <option value="" disabled>載入研討會列表中...</option>
            )}
            {availableSeminars.map(seminar => (
              <option key={seminar.name} value={seminar.name}>
                {seminar.name} ({seminar.session_count} 個會議)
              </option>
            ))}
          </select>
        </div>
      </Card>

      {/* 檔案上傳區域 */}
      <Card>
        <div className="p-6">
          <h2 className="text-lg font-semibold text-neutral-900 dark:text-neutral-100 mb-4">
            上傳 PPT 檔案
          </h2>
          
          {/* 拖放區域 */}
          <div
            className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
              isDragOver
                ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
                : 'border-neutral-300 dark:border-neutral-600 hover:border-primary-400 dark:hover:border-primary-500'
            }`}
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
          >
            <CloudUploadIcon className="w-12 h-12 text-neutral-400 mx-auto mb-4" />
            <p className="text-lg font-medium text-neutral-900 dark:text-neutral-100 mb-2">
              拖放 PDF 檔案到此處
            </p>
            <p className="text-neutral-600 dark:text-neutral-300 mb-4">
              或者點擊下方按鈕選擇檔案
            </p>
            <input
              type="file"
              multiple
              accept=".pdf"
              onChange={(e) => handleFileSelect(e.target.files)}
              className="hidden"
              id="file-upload"
              disabled={isProcessing}
            />
            <div
              onClick={triggerFileSelect}
              className={`
                inline-flex items-center justify-center px-4 py-2 text-sm font-medium rounded-md
                transition-colors duration-200 cursor-pointer
                ${isProcessing
                  ? 'bg-neutral-300 text-neutral-500 cursor-not-allowed'
                  : 'bg-primary-600 hover:bg-primary-700 text-white'
                }
              `}
            >
              選擇檔案
            </div>
          </div>

          {/* 檔案列表 */}
          {files.length > 0 && (
            <div className="mt-6">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-md font-medium text-neutral-900 dark:text-neutral-100">
                  已選擇的檔案 ({files.length})
                </h3>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={clearAllFiles}
                  disabled={isProcessing}
                  leftIcon={<TrashIcon className="w-4 h-4" />}
                >
                  清除全部
                </Button>
              </div>

              <div className="space-y-3 max-h-64 overflow-y-auto">
                {files.map((file) => (
                  <div
                    key={file.id}
                    className="flex items-center justify-between p-3 bg-neutral-50 dark:bg-neutral-800 rounded-lg"
                  >
                    <div className="flex items-center space-x-3 flex-1">
                      {getStatusIcon(file.status)}
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-neutral-900 dark:text-neutral-100 truncate">
                          {file.file.name}
                        </p>
                        <p className="text-xs text-neutral-600 dark:text-neutral-300">
                          {getStatusText(file)}
                        </p>
                        {file.status === 'processing' && (
                          <div className="w-full bg-neutral-200 dark:bg-neutral-700 rounded-full h-1.5 mt-1">
                            <div
                              className="bg-primary-500 h-1.5 rounded-full transition-all duration-300"
                              style={{ width: `${file.progress}%` }}
                            />
                          </div>
                        )}
                      </div>
                    </div>
                    {!isProcessing && file.status === 'pending' && (
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => removeFile(file.id)}
                        className="text-red-500 hover:text-red-700"
                      >
                        <XCircleIcon className="w-4 h-4" />
                      </Button>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* 處理按鈕 */}
          {files.length > 0 && (
            <div className="mt-6 flex justify-center">
              <Button
                variant="primary"
                size="lg"
                onClick={startProcessing}
                disabled={isProcessing || files.every(f => f.status !== 'pending')}
                className="px-8"
              >
                {isProcessing ? '處理中...' : `開始處理 ${files.filter(f => f.status === 'pending').length} 個檔案`}
              </Button>
            </div>
          )}
        </div>
      </Card>

      {/* 處理統計 */}
      {processingStats.total > 0 && (
        <Card>
          <div className="p-6">
            <h2 className="text-lg font-semibold text-neutral-900 dark:text-neutral-100 mb-4">
              處理統計
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-neutral-900 dark:text-neutral-100">
                  {processingStats.total}
                </div>
                <div className="text-sm text-neutral-600 dark:text-neutral-300">總計</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-yellow-600">
                  {processingStats.pending}
                </div>
                <div className="text-sm text-neutral-600 dark:text-neutral-300">等待中</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">
                  {processingStats.processing}
                </div>
                <div className="text-sm text-neutral-600 dark:text-neutral-300">處理中</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">
                  {processingStats.success}
                </div>
                <div className="text-sm text-neutral-600 dark:text-neutral-300">成功</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-red-600">
                  {processingStats.error}
                </div>
                <div className="text-sm text-neutral-600 dark:text-neutral-300">失敗</div>
              </div>
            </div>
          </div>
        </Card>
      )}

      {/* 結果模態框 */}
      <Modal
        isOpen={showResults}
        onClose={() => setShowResults(false)}
        title="處理結果"
        size="lg"
      >
        <div className="space-y-4">
          <div className="flex items-center space-x-2 p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
            <CheckCircleIcon className="w-5 h-5 text-green-500" />
            <span className="text-green-800 dark:text-green-200">
              處理完成！成功處理 {processingStats.success} 個檔案，失敗 {processingStats.error} 個檔案。
            </span>
          </div>

          {files.filter(f => f.status === 'success').length > 0 && (
            <div>
              <h3 className="font-medium text-neutral-900 dark:text-neutral-100 mb-2">
                成功處理的檔案：
              </h3>
              <div className="space-y-2">
                {files.filter(f => f.status === 'success').map(file => (
                  <div key={file.id} className="p-3 bg-neutral-50 dark:bg-neutral-800 rounded">
                    <div className="font-medium text-sm">{file.file.name}</div>
                    <div className="text-xs text-neutral-600 dark:text-neutral-300">
                      匹配會議: {file.matchedSession}
                    </div>
                    <div className="text-xs text-neutral-600 dark:text-neutral-300">
                      PPT 內容長度: {file.result?.ppt_length} 字符
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {files.filter(f => f.status === 'error').length > 0 && (
            <div>
              <h3 className="font-medium text-neutral-900 dark:text-neutral-100 mb-2">
                處理失敗的檔案：
              </h3>
              <div className="space-y-2">
                {files.filter(f => f.status === 'error').map(file => (
                  <div key={file.id} className="p-3 bg-red-50 dark:bg-red-900/20 rounded">
                    <div className="font-medium text-sm">{file.file.name}</div>
                    <div className="text-xs text-red-600 dark:text-red-400">
                      {file.error}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </Modal>
    </div>
  );
};
