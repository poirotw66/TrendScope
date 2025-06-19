
import { TrendData, Report, ReportStatus, Crawler, CrawlerStatus, ChartDataPoint, Notification } from '../types';

export const getMockTrendData = (count: number = 20): TrendData[] => {
  const mockPptContent = [
    '# AI 技術創新簡報\n\n## 概述\n本簡報介紹最新的 AI 技術發展趨勢...',
    '# 大模型應用實踐\n\n## 背景\n隨著大語言模型的快速發展...',
    '# 數據架構設計\n\n## 核心理念\n構建現代化的數據架構需要考慮...',
    '',  // 空內容表示沒有 PPT
    '# 雲端技術演進\n\n## 技術棧\n- 容器化\n- 微服務\n- 服務網格...'
  ];

  return Array.from({ length: count }, (_, i) => ({
    // BigQuery schema fields
    conference_id: `mock-${i + 1}`,
    seminar: `Mock Conference ${2023 + (i % 3)}`,
    name: `Session ${String.fromCharCode(65 + (i % 5))}-${i + 1}`,
    description: `This is a mock abstract for trend data item ${i + 1}. It discusses innovative approaches to AI and machine learning.`,
    url: `https://example.com/conf/${2023 + (i % 3)}/session${i + 1}`,
    pdf_url: i % 3 === 0 ? `https://example.com/pdf/session${i + 1}.pdf` : '',
    ppt_context: mockPptContent[i % mockPptContent.length],
    tags: [['AI', 'Machine Learning', 'Big Data', 'Cloud Computing', 'Cybersecurity'][i % 5]],
    created_at: new Date(2023, i % 12, (i % 28) + 1).toISOString(),

    // Legacy fields for backward compatibility
    id: `trend-${i + 1}`,
    conference: `Tech Conference ${2023 + (i % 3)}`,
    date: new Date(2023, i % 12, (i % 28) + 1).toISOString().split('T')[0],
    meeting: `Session ${String.fromCharCode(65 + (i % 5))}-${i + 1}`,
    abstract: `This is a mock abstract for trend data item ${i + 1}. It discusses innovative approaches to AI and machine learning.`,
    topic: ['AI', 'Machine Learning', 'Big Data', 'Cloud Computing', 'Cybersecurity'][i % 5],
    other: i % 4 === 0 ? `Some additional notes for item ${i+1}` : undefined,
  }));
};

export const getMockReports = (count: number = 10): Report[] => {
  return Array.from({ length: count }, (_, i) => ({
    id: `report-${i + 1}`,
    title: `Quarterly Tech Trends Report Q${(i % 4) + 1} ${2023 + Math.floor(i / 4)}`,
    date: new Date(2023, (i*3) % 12, (i % 28) + 1).toISOString().split('T')[0],
    responsiblePerson: ['Alice Johnson', 'Bob Williams', 'Carol Davis'][i % 3],
    status: i % 3 === 0 ? ReportStatus.PUBLISHED : ReportStatus.DRAFT,
  }));
};

export const getMockCrawlers = (count: number = 8): Crawler[] => {
  return Array.from({ length: count }, (_, i) => ({
    id: `crawler-${i + 1}`,
    name: `Crawler Task ${String.fromCharCode(65 + i)}`,
    source: ['TechNews.com', 'ScienceDaily', 'ResearchGate', 'arXiv'][i % 4],
    status: [CrawlerStatus.ENABLED, CrawlerStatus.DISABLED, CrawlerStatus.ERROR][i % 3],
    lastRunTime: new Date(Date.now() - i * 3600000 * 24).toLocaleString(),
  }));
};

export const getMockChartData = (points: number = 7, labelPrefix: string = "Day"): ChartDataPoint[] => {
  return Array.from({ length: points }, (_, i) => ({
    name: `${labelPrefix} ${i + 1}`,
    value: Math.floor(Math.random() * 100) + 10,
  }));
};

export const getMockDashboardStats = () => ({
  currentTasks: Math.floor(Math.random() * 50) + 5,
  summariesToday: Math.floor(Math.random() * 200) + 20,
  pendingReports: Math.floor(Math.random() * 10) + 1,
  systemAlerts: Math.floor(Math.random() * 5),
});

export const getMockNotifications = (count: number = 3) : Omit<Notification, 'id'|'read'>[] => {
  const types: Notification['type'][] = ['info', 'success', 'warning', 'error'];
  return Array.from({length: count}, (_, i) => ({
    message: `This is mock notification ${i+1}. Something important happened.`,
    type: types[i % types.length],
    timestamp: new Date(Date.now() - i * 60000 * 15) // 15 mins ago, 30 mins ago etc.
  }));
};
