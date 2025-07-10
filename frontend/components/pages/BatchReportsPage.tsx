import React, { useState, useEffect } from 'react';
import { Card } from '../ui/Card';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';
import { useAppContext } from '../../hooks/useAppContext';
import { useLanguage } from '../../hooks/useLanguage';
import { apiService } from '../../services/api';
import { DocumentReportIcon, PlayIcon, CheckIcon, XIcon, ClockIcon } from '../../constants';

interface SeminarInfo {
  name: string;
  session_count: number;
  sessions_with_ppt: number;
}

interface BatchReportTask {
  task_id: string;
  status: string;
  progress: {
    current: number;
    total: number;
    current_session: string;
  };
  start_time?: string;
  end_time?: string;
  error_message?: string;
  results?: {
    processed_sessions: number;
    failed_sessions: number;
    output_directory: string;
    md_directory: string;
    html_directory?: string;
  };
}

export const BatchReportsPage: React.FC = () => {
  const { setPageTitle } = useAppContext();
  const { t } = useLanguage();
  
  const [seminars, setSeminars] = useState<SeminarInfo[]>([]);
  const [selectedSeminars, setSelectedSeminars] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [currentTask, setCurrentTask] = useState<BatchReportTask | null>(null);
  const [limit, setLimit] = useState<string>('');
  const [includeHtml, setIncludeHtml] = useState(true);
  const [analysisMode, setAnalysisMode] = useState<string>('comprehensive');
  const [outputTemplate, setOutputTemplate] = useState<string>('professional');
  const [enableTrendAnalysis, setEnableTrendAnalysis] = useState<boolean>(true);
  const [enableRecommendations, setEnableRecommendations] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setPageTitle(t('batchReports', 'sidebar'));
    loadSeminars();
  }, [setPageTitle, t]);

  const loadSeminars = async () => {
    setLoading(true);
    setError(null);
    try {
      console.log('正在載入研討會列表...');
      const response = await apiService.getAvailableSeminarsForReports();
      console.log('研討會列表載入成功:', response);
      setSeminars(response.seminars);
    } catch (error: any) {
      console.error('載入研討會列表失敗:', error);
      setError(`載入研討會列表失敗: ${error.message || '未知錯誤'}`);
    } finally {
      setLoading(false);
    }
  };

  const handleSeminarToggle = (seminarName: string) => {
    setSelectedSeminars(prev => 
      prev.includes(seminarName)
        ? prev.filter(s => s !== seminarName)
        : [...prev, seminarName]
    );
  };

  const handleSelectAll = () => {
    if (selectedSeminars.length === seminars.length) {
      setSelectedSeminars([]);
    } else {
      setSelectedSeminars(seminars.map(s => s.name));
    }
  };

  const handleGenerateReports = async () => {
    if (selectedSeminars.length === 0) {
      setError('請至少選擇一個研討會');
      return;
    }

    setGenerating(true);
    setError(null);
    
    try {
      console.log('正在啟動批量報告生成...');
      const request = {
        seminars: selectedSeminars,
        limit: limit ? parseInt(limit) : undefined,
        output_format: 'markdown',
        include_html: includeHtml,
        analysis_mode: analysisMode,
        output_template: outputTemplate,
        enable_trend_analysis: enableTrendAnalysis,
        enable_recommendations: enableRecommendations
      };

      const response = await apiService.generateBatchReports(request);
      console.log('批量報告生成已啟動:', response);
      
      // 開始輪詢任務狀態
      setCurrentTask({
        task_id: response.task_id,
        status: response.status,
        progress: { current: 0, total: 0, current_session: '等待開始...' }
      });
      
      pollTaskStatus(response.task_id);
      
    } catch (error: any) {
      console.error('啟動報告生成失敗:', error);
      setError(`啟動報告生成失敗: ${error.message || '未知錯誤'}`);
      setGenerating(false);
    }
  };

  const pollTaskStatus = async (taskId: string) => {
    try {
      const status = await apiService.getBatchReportStatus(taskId);
      console.log('任務狀態更新:', status);
      setCurrentTask(status);
      
      if (status.status === 'running' || status.status === 'pending') {
        // 繼續輪詢
        setTimeout(() => pollTaskStatus(taskId), 2000);
      } else {
        // 任務完成或失敗
        setGenerating(false);
        if (status.status === 'failed') {
          setError(status.error_message || '報告生成失敗');
        }
      }
    } catch (error: any) {
      console.error('獲取任務狀態失敗:', error);
      setError(`獲取任務狀態失敗: ${error.message || '未知錯誤'}`);
      setGenerating(false);
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

  return (
    <div className="space-y-6">
      {/* 頁面標題 */}
      <div className="flex items-center space-x-3">
        <DocumentReportIcon className="w-8 h-8 text-blue-600" />
        <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">
          {t('batchReports', 'sidebar')}
        </h1>
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

      {/* 研討會選擇 */}
      <Card>
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100">
              選擇研討會
            </h2>
            <Button
              variant="secondary"
              size="sm"
              onClick={handleSelectAll}
              disabled={loading || generating}
            >
              {selectedSeminars.length === seminars.length ? '取消全選' : '全選'}
            </Button>
          </div>

          {loading ? (
            <div className="text-center py-8">
              <ClockIcon className="w-8 h-8 text-gray-400 animate-spin mx-auto mb-2" />
              <p className="text-gray-500">載入研討會列表中...</p>
            </div>
          ) : seminars.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-gray-500">沒有找到可用的研討會</p>
              <Button
                variant="secondary"
                size="sm"
                onClick={loadSeminars}
                className="mt-2"
              >
                重新載入
              </Button>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {seminars.map((seminar) => (
                <div
                  key={seminar.name}
                  className={`p-4 border rounded-lg cursor-pointer transition-colors ${
                    selectedSeminars.includes(seminar.name)
                      ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                      : 'border-gray-200 dark:border-gray-700 hover:border-blue-300'
                  }`}
                  onClick={() => !generating && handleSeminarToggle(seminar.name)}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <h3 className="font-medium text-gray-900 dark:text-gray-100">
                        {seminar.name}
                      </h3>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        總會議: {seminar.session_count} | 有PPT: {seminar.sessions_with_ppt}
                      </p>
                    </div>
                    <div className="ml-4">
                      {selectedSeminars.includes(seminar.name) && (
                        <CheckIcon className="w-5 h-5 text-blue-600" />
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </Card>

      {/* 生成選項 */}
      <Card>
        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100">
            生成選項
          </h2>
          
          {/* 分析模式選擇 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              分析模式
            </label>
            <select
              value={analysisMode}
              onChange={(e) => setAnalysisMode(e.target.value)}
              disabled={generating}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="technical">技術深度分析 - 專注於技術實現細節和架構分析</option>
              <option value="business">商業價值分析 - 重點分析商業應用和市場價值</option>
              <option value="trend">趨勢洞察分析 - 著重於技術趨勢和未來發展方向</option>
              <option value="comprehensive">綜合全面分析 - 包含技術、商業和趨勢的全方位分析</option>
            </select>
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
              選擇報告分析的深度和重點方向
            </p>
          </div>

          {/* 輸出樣板選擇 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              輸出樣板
            </label>
            <select
              value={outputTemplate}
              onChange={(e) => setOutputTemplate(e.target.value)}
              disabled={generating}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="professional">專業商務風格 - 正式的企業報告格式</option>
              <option value="technical">技術文檔風格 - 適合技術團隊的詳細文檔格式</option>
              <option value="concise">簡潔摘要風格 - 重點突出的簡潔版本</option>
              <option value="presentation">演示文稿風格 - 適合展示的視覺化格式</option>
            </select>
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
              選擇生成報告的外觀和格式風格
            </p>
          </div>

          {/* 增強功能選項 */}
          <div className="space-y-3">
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              增強功能 (基於 plan.md 的智慧化功能)
            </label>

            <div className="space-y-2">
              <label className="flex items-center space-x-3">
                <input
                  type="checkbox"
                  checked={enableTrendAnalysis}
                  onChange={(e) => setEnableTrendAnalysis(e.target.checked)}
                  disabled={generating}
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <div>
                  <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    🔍 LLM 趨勢分析
                  </span>
                  <p className="text-xs text-gray-500 dark:text-gray-400">
                    使用 Gemini 2.5 Flash 自動識別五大技術趨勢，生成趨勢關聯性分析
                  </p>
                </div>
              </label>

              <label className="flex items-center space-x-3">
                <input
                  type="checkbox"
                  checked={enableRecommendations}
                  onChange={(e) => setEnableRecommendations(e.target.checked)}
                  disabled={generating}
                  className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                />
                <div>
                  <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    🎯 智慧推薦引擎
                  </span>
                  <p className="text-xs text-gray-500 dark:text-gray-400">
                    基於內容分析生成個性化推薦和相關會議建議
                  </p>
                </div>
              </label>
            </div>

            <div className="bg-blue-50 dark:bg-blue-900/20 p-3 rounded-lg">
              <p className="text-xs text-blue-700 dark:text-blue-300">
                💡 啟用增強功能將生成符合 plan.md 規範的三階層報告結構：
                <br />• 趨勢分析總覽 (trends-analysis.md)
                <br />• 趨勢分類頁面 (trends/trend-*.md)
                <br />• 會議詳細頁面 (sessions/session-*.md)
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                會議數量限制（可選）
              </label>
              <Input
                type="number"
                placeholder="留空表示無限制"
                value={limit}
                onChange={(e) => setLimit(e.target.value)}
                disabled={generating}
                min="1"
              />
            </div>

            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                id="includeHtml"
                checked={includeHtml}
                onChange={(e) => setIncludeHtml(e.target.checked)}
                disabled={generating}
                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <label htmlFor="includeHtml" className="text-sm font-medium text-gray-700 dark:text-gray-300">
                同時生成 HTML 報告
              </label>
            </div>
          </div>
        </div>
      </Card>

      {/* 生成按鈕 */}
      <Card>
        <div className="flex justify-between items-center">
          <div>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              已選擇 {selectedSeminars.length} 個研討會
            </p>
            {selectedSeminars.length > 0 && (
              <p className="text-xs text-gray-500 dark:text-gray-500 mt-1">
                預計處理 {seminars.filter(s => selectedSeminars.includes(s.name)).reduce((sum, s) => sum + s.sessions_with_ppt, 0)} 個會議
              </p>
            )}
          </div>

          <Button
            variant="primary"
            size="lg"
            onClick={handleGenerateReports}
            disabled={generating || selectedSeminars.length === 0}
            leftIcon={generating ? <ClockIcon className="w-5 h-5 animate-spin" /> : <PlayIcon className="w-5 h-5" />}
          >
            {generating ? '生成中...' : '開始生成報告'}
          </Button>
        </div>
      </Card>

      {/* 任務狀態 */}
      {currentTask && (
        <Card>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100">
                生成進度
              </h2>
              <div className="flex items-center space-x-2">
                {getStatusIcon(currentTask.status)}
                <span className="text-sm font-medium">
                  {getStatusText(currentTask.status)}
                </span>
              </div>
            </div>

            {currentTask.progress && (
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>進度: {currentTask.progress.current} / {currentTask.progress.total}</span>
                  <span>
                    {currentTask.progress.total > 0
                      ? `${Math.round((currentTask.progress.current / currentTask.progress.total) * 100)}%`
                      : '0%'
                    }
                  </span>
                </div>
                <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                  <div
                    className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                    style={{
                      width: currentTask.progress.total > 0
                        ? `${(currentTask.progress.current / currentTask.progress.total) * 100}%`
                        : '0%'
                    }}
                  />
                </div>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {currentTask.progress.current_session}
                </p>
              </div>
            )}

            {currentTask.results && (
              <div className="mt-4 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                <h3 className="font-medium text-gray-900 dark:text-gray-100 mb-2">
                  生成結果
                </h3>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="text-gray-600 dark:text-gray-400">成功處理:</span>
                    <span className="ml-2 font-medium text-green-600">
                      {currentTask.results.processed_sessions}
                    </span>
                  </div>
                  <div>
                    <span className="text-gray-600 dark:text-gray-400">處理失敗:</span>
                    <span className="ml-2 font-medium text-red-600">
                      {currentTask.results.failed_sessions}
                    </span>
                  </div>
                </div>
                <div className="mt-2 text-sm">
                  <span className="text-gray-600 dark:text-gray-400">輸出目錄:</span>
                  <span className="ml-2 font-mono text-xs bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded">
                    {currentTask.results.output_directory}
                  </span>
                </div>
              </div>
            )}
          </div>
        </Card>
      )}
    </div>
  );
};
