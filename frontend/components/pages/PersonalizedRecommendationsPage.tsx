import React, { useState, useEffect } from 'react';
import { Card } from '../ui/Card';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';
import { useAppContext } from '../../hooks/useAppContext';
import { useLanguage } from '../../hooks/useLanguage';
import { apiService } from '../../services/api';
import { 
  SparklesIcon, 
  UserIcon, 
  HeartIcon, 
  StarIcon,
  EyeIcon,
  XIcon,
  PlusIcon,
  TrashIcon
} from '../../constants';

interface RecommendationItem {
  item_id: string;
  item_type: 'session' | 'trend' | 'topic';
  title: string;
  description: string;
  relevance_score: number;
  reasoning: string;
  metadata: {
    trends?: string[];
    confidence_scores?: Record<string, number>;
    session_data?: any;
    recommendation_type?: string;
  };
}

interface RecommendationResult {
  recommendations: RecommendationItem[];
  user_profile: {
    interests: string[];
    preferred_trends: string[];
    expertise_level: string;
  };
  statistics: {
    total_recommendations: number;
    total_sessions: number;
    total_trends: number;
  };
}

export const PersonalizedRecommendationsPage: React.FC = () => {
  const { setPageTitle } = useAppContext();
  const { t } = useLanguage();
  
  // 用戶興趣配置
  const [interests, setInterests] = useState<string[]>(['AI', '機器學習']);
  const [newInterest, setNewInterest] = useState('');
  const [preferredTrends, setPreferredTrends] = useState<string[]>([]);
  const [newTrend, setNewTrend] = useState('');
  const [expertiseLevel, setExpertiseLevel] = useState<string>('intermediate');
  const [maxRecommendations, setMaxRecommendations] = useState<string>('10');
  
  // 分析配置
  const [seminars, setSeminars] = useState<string[]>([]);
  const [selectedSeminars, setSelectedSeminars] = useState<string[]>([]);
  const [limit, setLimit] = useState<string>('50');
  
  // 狀態管理
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [recommendations, setRecommendations] = useState<RecommendationResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setPageTitle('個性化推薦');
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

  const handleAddInterest = () => {
    if (newInterest.trim() && !interests.includes(newInterest.trim())) {
      setInterests([...interests, newInterest.trim()]);
      setNewInterest('');
    }
  };

  const handleRemoveInterest = (interest: string) => {
    setInterests(interests.filter(i => i !== interest));
  };

  const handleAddTrend = () => {
    if (newTrend.trim() && !preferredTrends.includes(newTrend.trim())) {
      setPreferredTrends([...preferredTrends, newTrend.trim()]);
      setNewTrend('');
    }
  };

  const handleRemoveTrend = (trend: string) => {
    setPreferredTrends(preferredTrends.filter(t => t !== trend));
  };

  const handleGenerateRecommendations = async () => {
    if (interests.length === 0) {
      setError('請至少添加一個興趣領域');
      return;
    }

    setGenerating(true);
    setError(null);
    
    try {
      console.log('正在生成個性化推薦...');
      const response = await apiService.getPersonalizedRecommendations({
        user_interests: interests,
        preferred_trends: preferredTrends.length > 0 ? preferredTrends : undefined,
        expertise_level: expertiseLevel,
        max_recommendations: parseInt(maxRecommendations) || 10,
        seminars: selectedSeminars.length > 0 ? selectedSeminars : undefined,
        limit: limit ? parseInt(limit) : 50
      });
      
      console.log('個性化推薦完成:', response);
      setRecommendations(response);
    } catch (error: any) {
      console.error('生成推薦失敗:', error);
      setError(`生成推薦失敗: ${error.message}`);
    } finally {
      setGenerating(false);
    }
  };

  const getRelevanceColor = (score: number) => {
    if (score >= 0.8) return 'text-green-600 bg-green-100 dark:bg-green-900/20';
    if (score >= 0.6) return 'text-blue-600 bg-blue-100 dark:bg-blue-900/20';
    return 'text-gray-600 bg-gray-100 dark:bg-gray-800';
  };

  const getRelevanceLabel = (score: number) => {
    if (score >= 0.8) return '高度相關';
    if (score >= 0.6) return '中度相關';
    return '一般相關';
  };

  const getItemTypeIcon = (type: string) => {
    switch (type) {
      case 'session': return '📅';
      case 'trend': return '📈';
      case 'topic': return '💡';
      default: return '📄';
    }
  };

  const getItemTypeLabel = (type: string) => {
    switch (type) {
      case 'session': return '會議';
      case 'trend': return '趨勢';
      case 'topic': return '主題';
      default: return '項目';
    }
  };

  return (
    <div className="space-y-6">
      {/* 頁面標題 */}
      <div className="flex items-center space-x-3">
        <SparklesIcon className="w-8 h-8 text-pink-600" />
        <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100">
          個性化推薦
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

      {/* 用戶興趣配置 */}
      <Card>
        <div className="space-y-6">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100 flex items-center space-x-2">
            <UserIcon className="w-6 h-6 text-pink-600" />
            <span>個人興趣檔案</span>
          </h2>

          {/* 興趣領域 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              興趣領域 *
            </label>
            <div className="flex flex-wrap gap-2 mb-3">
              {interests.map(interest => (
                <span key={interest} className="inline-flex items-center px-3 py-1 bg-pink-100 dark:bg-pink-900/20 text-pink-700 dark:text-pink-300 rounded-full text-sm">
                  {interest}
                  <button
                    onClick={() => handleRemoveInterest(interest)}
                    className="ml-2 text-pink-500 hover:text-pink-700"
                  >
                    <XIcon className="w-3 h-3" />
                  </button>
                </span>
              ))}
            </div>
            <div className="flex space-x-2">
              <Input
                value={newInterest}
                onChange={(e) => setNewInterest(e.target.value)}
                placeholder="添加興趣領域 (如: AI, 區塊鏈, 雲計算)"
                onKeyPress={(e) => e.key === 'Enter' && handleAddInterest()}
                className="flex-1"
              />
              <Button
                variant="secondary"
                onClick={handleAddInterest}
                leftIcon={<PlusIcon className="w-4 h-4" />}
              >
                添加
              </Button>
            </div>
          </div>

          {/* 偏好趨勢 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              偏好技術趨勢 (可選)
            </label>
            <div className="flex flex-wrap gap-2 mb-3">
              {preferredTrends.map(trend => (
                <span key={trend} className="inline-flex items-center px-3 py-1 bg-blue-100 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 rounded-full text-sm">
                  {trend}
                  <button
                    onClick={() => handleRemoveTrend(trend)}
                    className="ml-2 text-blue-500 hover:text-blue-700"
                  >
                    <XIcon className="w-3 h-3" />
                  </button>
                </span>
              ))}
            </div>
            <div className="flex space-x-2">
              <Input
                value={newTrend}
                onChange={(e) => setNewTrend(e.target.value)}
                placeholder="添加偏好趨勢 (如: AI 晶片與硬體加速)"
                onKeyPress={(e) => e.key === 'Enter' && handleAddTrend()}
                className="flex-1"
              />
              <Button
                variant="secondary"
                onClick={handleAddTrend}
                leftIcon={<PlusIcon className="w-4 h-4" />}
              >
                添加
              </Button>
            </div>
          </div>

          {/* 專業程度 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              專業程度
            </label>
            <select
              value={expertiseLevel}
              onChange={(e) => setExpertiseLevel(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
            >
              <option value="beginner">初學者 - 剛接觸相關技術</option>
              <option value="intermediate">中級 - 有一定基礎和經驗</option>
              <option value="expert">專家 - 深度專業知識和豐富經驗</option>
            </select>
          </div>

          {/* 推薦數量 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              推薦數量
            </label>
            <Input
              type="number"
              value={maxRecommendations}
              onChange={(e) => setMaxRecommendations(e.target.value)}
              placeholder="10"
              className="w-32"
              min="1"
              max="50"
            />
          </div>
        </div>
      </Card>

      {/* 數據範圍配置 */}
      <Card>
        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100">
            數據範圍配置
          </h2>

          {/* 研討會選擇 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              研討會範圍 (可選，留空則分析所有研討會)
            </label>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2 max-h-32 overflow-y-auto">
              {seminars.map(seminar => (
                <label key={seminar} className="flex items-center space-x-2 p-2 rounded hover:bg-gray-50 dark:hover:bg-gray-800">
                  <input
                    type="checkbox"
                    checked={selectedSeminars.includes(seminar)}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setSelectedSeminars([...selectedSeminars, seminar]);
                      } else {
                        setSelectedSeminars(selectedSeminars.filter(s => s !== seminar));
                      }
                    }}
                    className="rounded border-gray-300 text-pink-600 focus:ring-pink-500"
                  />
                  <span className="text-sm text-gray-700 dark:text-gray-300">{seminar}</span>
                </label>
              ))}
            </div>
          </div>

          {/* 數據限制 */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              分析會議數量限制
            </label>
            <Input
              type="number"
              value={limit}
              onChange={(e) => setLimit(e.target.value)}
              placeholder="50"
              className="w-32"
            />
          </div>

          {/* 生成按鈕 */}
          <div className="flex justify-between items-center pt-4 border-t border-gray-200 dark:border-gray-700">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                基於 {interests.length} 個興趣領域生成推薦
              </p>
            </div>
            <Button
              variant="primary"
              size="lg"
              onClick={handleGenerateRecommendations}
              disabled={generating || interests.length === 0}
              leftIcon={generating ? <SparklesIcon className="w-5 h-5 animate-spin" /> : <HeartIcon className="w-5 h-5" />}
            >
              {generating ? '生成中...' : '生成推薦'}
            </Button>
          </div>
        </div>
      </Card>

      {/* 推薦結果 */}
      {recommendations && (
        <div className="space-y-6">
          {/* 統計概覽 */}
          <Card>
            <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4">
              推薦統計
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="text-center p-4 bg-pink-50 dark:bg-pink-900/20 rounded-lg">
                <div className="text-2xl font-bold text-pink-600">{recommendations.statistics.total_recommendations}</div>
                <div className="text-sm text-gray-600 dark:text-gray-400">推薦項目</div>
              </div>
              <div className="text-center p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                <div className="text-2xl font-bold text-blue-600">{recommendations.statistics.total_sessions}</div>
                <div className="text-sm text-gray-600 dark:text-gray-400">分析會議</div>
              </div>
              <div className="text-center p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
                <div className="text-2xl font-bold text-green-600">{recommendations.statistics.total_trends}</div>
                <div className="text-sm text-gray-600 dark:text-gray-400">識別趨勢</div>
              </div>
            </div>
          </Card>

          {/* 推薦列表 */}
          <Card>
            <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100 mb-4 flex items-center space-x-2">
              <StarIcon className="w-6 h-6 text-yellow-600" />
              <span>為您推薦</span>
            </h2>
            <div className="space-y-4">
              {recommendations.recommendations
                .sort((a, b) => b.relevance_score - a.relevance_score)
                .map((item, index) => (
                <div key={item.item_id} className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:shadow-md transition-shadow">
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center space-x-3">
                      <div className="text-2xl">{getItemTypeIcon(item.item_type)}</div>
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                          {item.title}
                        </h3>
                        <div className="flex items-center space-x-2 mt-1">
                          <span className="text-xs text-gray-500 bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded">
                            {getItemTypeLabel(item.item_type)}
                          </span>
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getRelevanceColor(item.relevance_score)}`}>
                            {getRelevanceLabel(item.relevance_score)} ({item.relevance_score.toFixed(2)})
                          </span>
                        </div>
                      </div>
                    </div>
                    <div className="text-2xl font-bold text-gray-400">#{index + 1}</div>
                  </div>
                  
                  <p className="text-gray-700 dark:text-gray-300 mb-3">
                    {item.description}
                  </p>
                  
                  <div className="bg-blue-50 dark:bg-blue-900/20 p-3 rounded-lg mb-3">
                    <div className="text-sm font-medium text-blue-700 dark:text-blue-300 mb-1">推薦理由:</div>
                    <p className="text-blue-600 dark:text-blue-400 text-sm">{item.reasoning}</p>
                  </div>
                  
                  {item.metadata.trends && item.metadata.trends.length > 0 && (
                    <div className="flex flex-wrap gap-2">
                      <span className="text-sm text-gray-500">相關趨勢:</span>
                      {item.metadata.trends.map(trend => (
                        <span key={trend} className="px-2 py-1 bg-purple-100 dark:bg-purple-900/20 text-purple-700 dark:text-purple-300 rounded text-sm">
                          {trend}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </Card>
        </div>
      )}
    </div>
  );
};
