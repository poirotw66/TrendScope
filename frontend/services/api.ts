/**
 * API 服務
 * 提供與後端 API 通信的方法
 */
import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';

// API 基礎配置
const apiConfig = {
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  timeout: 30000,
};

// API 響應類型定義
export interface ApiResponse<T> {
  data: T;
  status: number;
  statusText: string;
}

// 爬蟲請求參數
export interface ScraperRequest {
  scraper_type: string;
  headless?: boolean;
  wait_time?: number;
  use_bigquery?: boolean;
}

// 爬蟲回應類型
export interface ScraperResponse {
  task_id: string;
  message: string;
  status: string;
}

// 爬蟲結果類型
export interface ScraperResult {
  task_id: string;
  status: string;
  file_path?: string;
  message?: string;
  data?: any[];
}

// 會議類型
export interface Session {
  id: string;
  name: string;
  source: string;
  url?: string;
  description?: string;
  start_date?: string;
  end_date?: string;
  location?: string;
  tags?: string[];
  speakers?: {
    name: string;
    title?: string;
    company?: string;
  }[];
  created_at: string;
  updated_at: string;
}

/**
 * API 服務類
 */
class ApiService {
  private api: AxiosInstance;

  constructor() {
    // 創建 axios 實例
    this.api = axios.create(apiConfig);

    // 請求攔截器
    this.api.interceptors.request.use(
      (config) => {
        // 在這裡可以添加認證令牌等
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // 響應攔截器
    this.api.interceptors.response.use(
      (response) => {
        return response;
      },
      (error) => {
        // 處理錯誤響應
        console.error('API 錯誤:', error.response?.data || error.message);
        return Promise.reject(error);
      }
    );
  }

  /**
   * 獲取所有可用的爬蟲
   * @returns 可用爬蟲列表
   */
  public async getAvailableScrapers(): Promise<{ id: string; name: string; description: string }[]> {
    const response = await this.api.get('/scrapers/list');
    return response.data.scrapers;
  }

  /**
   * 運行爬蟲
   * @param request 爬蟲請求參數
   * @returns 爬蟲響應
   */
  public async runScraper(request: ScraperRequest): Promise<ScraperResponse> {
    const response = await this.api.post('/scrapers/run', request);
    return response.data;
  }

  /**
   * 獲取爬蟲任務狀態
   * @param taskId 任務 ID
   * @returns 爬蟲結果
   */
  public async getScraperStatus(taskId: string): Promise<ScraperResult> {
    const response = await this.api.get(`/scrapers/status/${taskId}`);
    return response.data;
  }

  /**
   * 獲取會議資料
   * @param source 可選的資料來源過濾
   * @param limit 最大結果數量
   * @returns 會議資料列表
   */
  public async getSessions(source?: string, limit: number = 20): Promise<Session[]> {
    const params: Record<string, any> = { limit };
    if (source) {
      params.source = source;
    }

    const response = await this.api.get('/data/sessions', { params });
    return response.data.sessions;
  }
}

// 導出 API 服務實例
export const apiService = new ApiService();
export default apiService;
