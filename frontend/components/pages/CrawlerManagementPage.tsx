import React, { useEffect, useState } from 'react';
import apiService, { ScraperRequest, ScraperResult } from '../../services/api';
import { Card } from '../ui/Card';
import { Button } from '../ui/Button';
import { PlayIcon } from '../../constants';

export const CrawlerManagementPage: React.FC = () => {
  const [scrapers, setScrapers] = useState<{ id: string; name: string; description: string }[]>([]);
  const [selectedScraper, setSelectedScraper] = useState<string>('');
  const [headless, setHeadless] = useState<boolean>(true);
  const [waitTime, setWaitTime] = useState<number>(30);
  const [useBigQuery, setUseBigQuery] = useState<boolean>(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [taskId, setTaskId] = useState<string | null>(null);
  const [taskStatus, setTaskStatus] = useState<ScraperResult | null>(null);
  const [pollingInterval, setPollingInterval] = useState<NodeJS.Timeout | null>(null);

  useEffect(() => {
    const fetchScrapers = async () => {
      try {
        setLoading(true);
        const availableScrapers = await apiService.getAvailableScrapers();
        setScrapers(availableScrapers);
        if (availableScrapers.length > 0) {
          setSelectedScraper(availableScrapers[0].id);
        }
      } catch (err) {
        setError('無法獲取爬蟲列表，請確保 API 服務正在運行');
      } finally {
        setLoading(false);
      }
    };
    fetchScrapers();
    return () => { if (pollingInterval) clearInterval(pollingInterval); };
    // eslint-disable-next-line
  }, []);

  const startPolling = (taskId: string) => {
    if (pollingInterval) clearInterval(pollingInterval);
    const interval = setInterval(async () => {
      try {
        const result = await apiService.getScraperStatus(taskId);
        setTaskStatus(result);
        if (result.status === 'completed' || result.status === 'failed') {
          clearInterval(interval);
          setPollingInterval(null);
        }
      } catch {
        clearInterval(interval);
        setPollingInterval(null);
      }
    }, 3000);
    setPollingInterval(interval);
  };

  const handleRunScraper = async () => {
    try {
      setLoading(true);
      setError(null);
      setTaskId(null);
      setTaskStatus(null);
      const request: ScraperRequest = {
        scraper_type: selectedScraper,
        headless,
        wait_time: waitTime,
        use_bigquery: useBigQuery
      };
      const response = await apiService.runScraper(request);
      setTaskId(response.task_id);
      startPolling(response.task_id);
    } catch (err: any) {
      setError(`運行爬蟲失敗: ${err.message || JSON.stringify(err)}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto py-8 space-y-6">
      <Card>
        <div className="mb-6">
          <h2 className="text-xl font-bold mb-2">爬蟲管理</h2>
          <p className="text-neutral-600 text-sm mb-2">選擇爬蟲、設定參數並執行。可即時查看任務狀態與結果。</p>
        </div>
        <form className="grid grid-cols-1 md:grid-cols-2 gap-4 items-center">
          <div>
            <label className="block mb-1 font-medium">選擇爬蟲</label>
            <select value={selectedScraper} onChange={e => setSelectedScraper(e.target.value)} disabled={loading} className="w-full border rounded px-2 py-1">
              {scrapers.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
            </select>
            <div className="text-xs text-neutral-500 mt-1 min-h-[1.5em]">
              {scrapers.find(s => s.id === selectedScraper)?.description}
            </div>
          </div>
          <div className="flex flex-col gap-2">
            <label className="inline-flex items-center">
              <input type="checkbox" checked={headless} onChange={e => setHeadless(e.target.checked)} disabled={loading} className="mr-2" />
              無頭模式（不顯示瀏覽器）
            </label>
            <label className="inline-flex items-center">
              <span className="mr-2">等待時間(秒)：</span>
              <input type="number" value={waitTime} min={5} max={120} onChange={e => setWaitTime(Number(e.target.value))} disabled={loading} className="w-20 border rounded px-1 py-0.5" />
            </label>
            <label className="inline-flex items-center">
              <input type="checkbox" checked={useBigQuery} onChange={e => setUseBigQuery(e.target.checked)} disabled={loading} className="mr-2" />
              將結果上傳到 BigQuery
            </label>
          </div>
          <div className="md:col-span-2 flex justify-end mt-2">
            <Button variant="primary" onClick={e => { e.preventDefault(); handleRunScraper(); }} disabled={loading || !selectedScraper} leftIcon={<PlayIcon className="w-4 h-4" />}>
              {loading ? '執行中...' : '執行爬蟲'}
            </Button>
          </div>
        </form>
        {error && <div className="text-red-500 text-sm mt-2">{error}</div>}
      </Card>
      {taskId && taskStatus && (
        <Card>
          <div className="mb-2 flex items-center gap-2">
            <span className="font-semibold">任務狀態：</span>
            <span className={`px-2 py-0.5 rounded text-xs font-bold ${taskStatus.status === 'completed' ? 'bg-green-100 text-green-700' : taskStatus.status === 'failed' ? 'bg-red-100 text-red-700' : 'bg-yellow-100 text-yellow-700'}`}>{taskStatus.status}</span>
          </div>
          <div className="mb-2 text-sm">{taskStatus.message}</div>
          {taskStatus.status === 'completed' && taskStatus.data && (
            <div className="mt-2">
              <div className="font-medium mb-1">爬取結果摘要（前 5 筆）：</div>
              <ul className="list-disc ml-6 text-sm">
                {taskStatus.data.slice(0, 5).map((item: any, idx: number) => (
                  <li key={idx} className="mb-1">
                    <span className="font-semibold">{item['會議名稱'] || item.name}</span>
                    {item['會議連結'] && <a href={item['會議連結']} target="_blank" rel="noopener noreferrer" className="ml-2 text-blue-600 underline">連結</a>}
                  </li>
                ))}
                {taskStatus.data.length > 5 && <li className="italic text-neutral-500">...還有 {taskStatus.data.length - 5} 筆</li>}
              </ul>
            </div>
          )}
        </Card>
      )}
    </div>
  );
};

export default CrawlerManagementPage;
