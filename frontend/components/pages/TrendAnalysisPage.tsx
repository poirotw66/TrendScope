import React, { useState, useEffect } from 'react';
import { Card } from '../ui/Card';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';
import { useAppContext } from '../../hooks/useAppContext';
import { useLanguage } from '../../hooks/useLanguage';
import { apiService } from '../../services/api';
import { 
  ChartBarIcon, 
  SparklesIcon, 
  EyeIcon, 
  ArrowTrendingUpIcon,
  LightBulbIcon,
  XIcon 
} from '../../constants';

interface TrendInfo {
  name: string;
  description: string;
  keywords: string[];
  importance_score: number;
  session_count: number;
}

interface SessionMapping {
  session_id: string;
  title: string;
  trends: string[];
  confidence_scores: Record<string, number>;
}

interface CorrelationAnalysis {
  correlation_insights: string[];
  trend_clusters: Array<{
    primary_trend: string;
    related_trends: Array<{
      trend: string;
      co_occurrence: number;
      similarity: number;
    }>;
    cluster_strength: number;
    description: string;
  }>;
  analysis_metadata: {
    total_sessions: number;
    mapped_sessions: number;
    analysis_timestamp: string;
  };
}

interface TrendAnalysisResult {
  trends: TrendInfo[];
  session_mappings: SessionMapping[];
  correlation_analysis: CorrelationAnalysis;
  statistics: {
    total_sessions: number;
    total_trends: number;
    mapped_sessions: number;
  };
}

export const TrendAnalysisPage: React.FC = () => {
  const { setPageTitle } = useAppContext();
  const { t } = useLanguage();
  
  const [seminars, setSeminars] = useState<string[]>([]);
  const [selectedSeminars, setSelectedSeminars] = useState<string[]>([]);
  const [limit, setLimit] = useState<string>('50');
  const [loading, setLoading] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<TrendAnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setPageTitle('技術趨勢分析');
    loadSeminars();
  }, [setPageTitle]);

  const loadSeminars = async () => {
    setLoading(true);
    try {
      const response = await apiService.getAvailableSeminarsForReports();
      setSeminars(response.seminars.map((s: any) => s.name));
    } catch (error: any) {
      console.error('載入研討會失敗:', error);
      setError(`載入研討會失敗: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyzeTrends = async () => {
    setAnalyzing(true);
    setError(null);
    
    try {
      console.log('正在執行趨勢分析...');
      const response = await apiService.analyzeTrends({
        seminars: selectedSeminars.length > 0 ? selectedSeminars : undefined,
        limit: limit ? parseInt(limit) : 50
      });
      
      console.log('趨勢分析完成:', response);
      setAnalysisResult(response);
    } catch (error: any) {
      console.error('趨勢分析失敗:', error);
      setError(`趨勢分析失敗: ${error.message}`);
    } finally {
      setAnalyzing(false);
    }
  };

  const handleSeminarToggle = (seminar: string) => {
    setSelectedSeminars(prev => 
      prev.includes(seminar) 
        ? prev.filter(s => s !== seminar)
        : [...prev, seminar]
    );
  };

  const getImportanceColor = (score: number) => {
    if (score >= 0.8) return 'text-red-600 bg-red-100 dark:bg-red-900/20';
    if (score >= 0.6) return 'text-orange-600 bg-orange-100 dark:bg-orange-900/20';
    return 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900/20';
  };

  const getImportanceLabel = (score: number) => {
    if (score >= 0.8) return '高度重要';
    if (score >= 0.6) return '中等重要';
    return '新興趨勢';
  };

  return (
    <div className="space-y-6">
      {/* 頁面標題 */}
      <div className="flex items-center space-x-3">
        <ChartBarIcon className="w-8 h-8 text-purple-600" />
        <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">
          技術趨勢分析
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

      {/* 分析配置 */}
      <Card>
        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100 flex items-center space-x-2">
            <SparklesIcon className="w-6 h-6 text-purple-600" />
            <span>分析配置</span>
          </h2>

          {/* 研討會選擇 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              選擇研討會 (可選，留空則分析所有研討會)
            </label>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2 max-h-40 overflow-y-auto">
              {seminars.map(seminar => (
                <label key={seminar} className="flex items-center space-x-2 p-2 rounded hover:bg-gray-50 dark:hover:bg-gray-800">
                  <input
                    type="checkbox"
                    checked={selectedSeminars.includes(seminar)}
                    onChange={() => handleSeminarToggle(seminar)}
                    disabled={analyzing}
                    className="rounded border-gray-300 text-purple-600 focus:ring-purple-500"
                  />
                  <span className="text-sm text-gray-700 dark:text-gray-300">{seminar}</span>
                </label>
              ))}
            </div>
          </div>

          {/* 分析限制 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              分析會議數量限制
            </label>
            <Input
              type="number"
              value={limit}
              onChange={(e) => setLimit(e.target.value)}
              disabled={analyzing}
              placeholder="50"
              className="w-32"
            />
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
              限制每個研討會分析的會議數量，留空則不限制
            </p>
          </div>

          {/* 分析按鈕 */}
          <div className="flex justify-between items-center pt-4 border-t border-gray-200 dark:border-gray-700">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                {selectedSeminars.length > 0 
                  ? `已選擇 ${selectedSeminars.length} 個研討會`
                  : '將分析所有研討會'
                }
              </p>
            </div>
            <Button
              variant="primary"
              size="lg"
              onClick={handleAnalyzeTrends}
              disabled={analyzing}
              leftIcon={analyzing ? <SparklesIcon className="w-5 h-5 animate-spin" /> : <ChartBarIcon className="w-5 h-5" />}
            >
              {analyzing ? '分析中...' : '開始趨勢分析'}
            </Button>
          </div>
        </div>
      </Card>

      {/* 分析結果 */}
      {analysisResult && (
        <div className="space-y-6">
          {/* 統計概覽 */}
          <Card>
            <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">
              分析統計
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="text-center p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                <div className="text-2xl font-bold text-blue-600">{analysisResult.statistics.total_sessions}</div>
                <div className="text-sm text-gray-600 dark:text-gray-400">總會議數</div>
              </div>
              <div className="text-center p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
                <div className="text-2xl font-bold text-green-600">{analysisResult.statistics.total_trends}</div>
                <div className="text-sm text-gray-600 dark:text-gray-400">識別趨勢</div>
              </div>
              <div className="text-center p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
                <div className="text-2xl font-bold text-purple-600">
                  {Math.round((analysisResult.statistics.mapped_sessions / analysisResult.statistics.total_sessions) * 100)}%
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-400">分類成功率</div>
              </div>
            </div>
          </Card>

          {/* 五大技術趨勢 */}
          <Card>
            <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4 flex items-center space-x-2">
              <ArrowTrendingUpIcon className="w-6 h-6 text-green-600" />
              <span>五大技術趨勢</span>
            </h2>
            <div className="space-y-4">
              {analysisResult.trends
                .sort((a, b) => b.importance_score - a.importance_score)
                .map((trend, index) => (
                <div key={trend.name} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center space-x-3">
                      <div className="text-2xl font-bold text-gray-400">#{index + 1}</div>
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                          {trend.name}
                        </h3>
                        <div className="flex items-center space-x-2 mt-1">
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getImportanceColor(trend.importance_score)}`}>
                            {getImportanceLabel(trend.importance_score)}
                          </span>
                          <span className="text-sm text-gray-500">
                            評分: {trend.importance_score.toFixed(2)}
                          </span>
                          <span className="text-sm text-gray-500">
                            相關會議: {trend.session_count} 場
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <p className="text-gray-700 dark:text-gray-300 mb-3">
                    {trend.description}
                  </p>
                  
                  <div className="flex flex-wrap gap-2">
                    {trend.keywords.map(keyword => (
                      <span key={keyword} className="px-2 py-1 bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded text-sm">
                        {keyword}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </Card>

          {/* 趨勢關聯性分析 */}
          {analysisResult.correlation_analysis.correlation_insights.length > 0 && (
            <Card>
              <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4 flex items-center space-x-2">
                <LightBulbIcon className="w-6 h-6 text-yellow-600" />
                <span>關聯性洞察</span>
              </h2>
              <div className="space-y-3">
                {analysisResult.correlation_analysis.correlation_insights.map((insight, index) => (
                  <div key={index} className="flex items-start space-x-3 p-3 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg">
                    <LightBulbIcon className="w-5 h-5 text-yellow-600 mt-0.5 flex-shrink-0" />
                    <p className="text-gray-700 dark:text-gray-300">{insight}</p>
                  </div>
                ))}
              </div>
            </Card>
          )}

          {/* 技術生態圈 */}
          {analysisResult.correlation_analysis.trend_clusters.length > 0 && (
            <Card>
              <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">
                技術生態圈
              </h2>
              <div className="space-y-4">
                {analysisResult.correlation_analysis.trend_clusters.map((cluster, index) => (
                  <div key={index} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">
                      {cluster.primary_trend} 生態圈
                    </h3>
                    <p className="text-gray-700 dark:text-gray-300 mb-3">
                      {cluster.description}
                    </p>
                    <div className="space-y-2">
                      <div className="text-sm font-medium text-gray-600 dark:text-gray-400">相關技術:</div>
                      {cluster.related_trends.map((related, idx) => (
                        <div key={idx} className="flex items-center justify-between p-2 bg-gray-50 dark:bg-gray-800 rounded">
                          <span className="text-gray-700 dark:text-gray-300">{related.trend}</span>
                          <div className="flex items-center space-x-2 text-sm text-gray-500">
                            <span>共現: {related.co_occurrence}次</span>
                            <span>相似度: {related.similarity.toFixed(2)}</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          )}
        </div>
      )}
    </div>
  );
};
