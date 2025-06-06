import time
import threading
from datetime import datetime, timedelta
from google import genai
from src.utils.logging_utils import logger
from config.config import (
    GEMINI_API_KEY, MAX_REQUESTS_PER_MINUTE, 
    REQUEST_INTERVAL, MAX_RETRIES, RETRY_DELAY
)

class GeminiAPI:
    """Gemini API 請求管理器，處理配額限制與重試邏輯"""
    
    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.api_requests = []
        self.api_counter_lock = threading.Lock()
    
    def wait_for_quota(self):
        """等待 API 配額可用"""
        current_time = datetime.now()
        with self.api_counter_lock:
            # 清理一分鐘前的請求記錄
            one_minute_ago = current_time - timedelta(minutes=1)
            self.api_requests = [req for req in self.api_requests if req >= one_minute_ago]
            
            # 檢查是否達到限制
            if len(self.api_requests) >= MAX_REQUESTS_PER_MINUTE:
                wait_time = (self.api_requests[0] + timedelta(minutes=1) - current_time).total_seconds()
                logger.info(f"API 請求達到限制，等待 {wait_time:.2f} 秒...")
                time.sleep(wait_time + 0.5)  # 額外等待 0.5 秒作為緩衝
                return self.wait_for_quota()
            
            # 記錄本次請求
            self.api_requests.append(current_time)
            return True
    
    def generate_content(self, prompt, model="gemini-2.0-flash"):
        """發送 API 請求並處理重試邏輯"""
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                # 等待配額
                self.wait_for_quota()
                
                # 發送請求
                response = self.client.models.generate_content(
                    model=model,
                    contents=[prompt]
                )
                
                # 檢查回應
                if not response or not hasattr(response, 'text'):
                    raise Exception("API 回應無效")
                
                return response.text
            except Exception as e:
                logger.error(f"API 請求錯誤 (嘗試 {attempt}/{MAX_RETRIES}): {e}")
                if attempt < MAX_RETRIES:
                    logger.info(f"等待 {RETRY_DELAY} 秒後重試...")
                    time.sleep(RETRY_DELAY)
                else:
                    logger.error("已達最大重試次數，放棄請求")
                    raise
            finally:
                # 每次請求後都等待，避免超過限制
                time.sleep(REQUEST_INTERVAL)

# 全域 API 實例
gemini_api = GeminiAPI()