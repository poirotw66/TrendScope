/**
 * API 服務
 * 提供與後端 API 通信的方法
 */
import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';
import { TrendData } from '../types';

// API 基礎配置
const apiConfig = {
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8001',
  timeout: 60000, // 增加到 60 秒，給上傳請求更多時間
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

// 會議類型 - 匹配 BigQuery schema
export interface Session {
  conference_id: string;
  seminar: string;
  name: string;
  description?: string;
  url?: string;
  pdf_url?: string;
  ppt_context?: string;
  tags?: string[];
  created_at: string;
  // Legacy fields for backward compatibility
  id?: string;
  source?: string;
  start_date?: string;
  end_date?: string;
  location?: string;
  speakers?: {
    name: string;
    title?: string;
    company?: string;
  }[];
  updated_at?: string;
}

/**
 * API 服務類
 */
class ApiService {
  private api: AxiosInstance;

  // 公開 api 實例以供直接訪問
  public get axiosInstance() {
    return this.api;
  }

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

  /**
   * 獲取資料庫管理頁面的會議資料 (轉換為 TrendData 格式)
   * @param source 可選的資料來源過濾
   * @param seminar 可選的研討會過濾
   * @param limit 最大結果數量
   * @returns TrendData 格式的會議資料列表
   */
  public async getTrendData(source?: string, seminar?: string, limit: number = 100): Promise<TrendData[]> {
    const params: Record<string, any> = { limit };
    if (source) {
      params.source = source;
    }
    if (seminar) {
      params.seminar = seminar;
    }

    const response = await this.api.get('/data/sessions', { params });
    const sessions: Session[] = response.data.sessions;

    // 轉換 Session 資料為 TrendData 格式
    return sessions.map((session, index) => ({
      // BigQuery schema fields - 直接使用 BigQuery 返回的欄位
      conference_id: session.conference_id || `session-${index}`,
      seminar: session.seminar || 'Unknown Seminar',
      name: session.name || 'Untitled Session',
      description: session.description || '',
      url: session.url || '',
      pdf_url: session.pdf_url || '',
      ppt_context: session.ppt_context || '',
      tags: session.tags || [],
      created_at: session.created_at,

      // Legacy fields for backward compatibility
      id: session.conference_id || session.id || `session-${index}`,
      conference: session.seminar || session.source || 'Unknown Conference',
      date: session.created_at ? new Date(session.created_at).toISOString().split('T')[0] : '',
      meeting: session.name || 'Untitled Session',
      abstract: session.description || '',
      topic: session.tags?.[0] || 'General',
      other: session.location || undefined,
    }));
  }

  /**
   * 上傳 PPT 檔案
   * @param files 要上傳的檔案列表
   * @param seminar 目標研討會
   * @returns 上傳響應
   */
  public async uploadPPTFiles(files: File[], seminar: string): Promise<any> {
    const formData = new FormData();

    files.forEach(file => {
      formData.append('files', file);
    });
    formData.append('seminar', seminar);

    // PPT 上傳需要更長的超時時間，因為檔案可能較大
    // 但實際上後端會立即返回 task_id，真正的處理在背景進行
    const response = await this.api.post('/ppt/upload', formData, {
      timeout: 120000, // 2分鐘超時，足夠檔案上傳和任務創建
    });

    return response.data;
  }

  /**
   * 獲取 PPT 處理狀態
   * @param taskId 任務 ID
   * @returns 處理狀態
   */
  public async getPPTProcessingStatus(taskId: string): Promise<any> {
    // 狀態查詢應該很快，使用較短的超時時間
    const response = await this.api.get(`/ppt/status/${taskId}`, {
      timeout: 15000, // 15秒超時
    });
    return response.data;
  }

  /**
   * 獲取可用的研討會列表
   * @returns 研討會列表
   */
  public async getAvailableSeminars(): Promise<any> {
    const response = await this.api.get('/ppt/seminars');
    return response.data;
  }
}

// 導出 API 服務實例
export const apiService = new ApiService();
export default apiService;
