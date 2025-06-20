"""
優化的 PowerPoint 解析和 BigQuery 上傳工具
解決性能瓶頸問題，實現並行處理和高效API調用
"""

import os
import sys
import time
import logging
import asyncio
import threading
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
import json

# 第三方庫
import pandas as pd
from google.cloud import bigquery
from google.cloud.bigquery import LoadJobConfig, WriteDisposition
from google import genai

# 本地模組
from .optimized_bigquery_client import OptimizedBigQueryClient

# 設置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class PPTProcessingResult:
    """PPT 處理結果"""
    file_path: Path
    success: bool
    content: Optional[str] = None
    conference_id: Optional[str] = None
    error: Optional[str] = None
    processing_time: float = 0.0

@dataclass
class ProcessingStats:
    """處理統計信息"""
    total_files: int = 0
    successful: int = 0
    failed: int = 0
    total_time: float = 0.0
    avg_time_per_file: float = 0.0

class RateLimiter:
    """API 速率限制器"""
    
    def __init__(self, max_requests_per_minute: int = 15):
        self.max_requests = max_requests_per_minute
        self.requests = Queue()
        self.lock = threading.Lock()
    
    def acquire(self):
        """獲取API調用許可"""
        with self.lock:
            now = time.time()
            
            # 清理超過1分鐘的請求記錄
            while not self.requests.empty():
                if now - self.requests.queue[0] > 60:
                    self.requests.get()
                else:
                    break
            
            # 檢查是否超過限制
            if self.requests.qsize() >= self.max_requests:
                sleep_time = 60 - (now - self.requests.queue[0])
                if sleep_time > 0:
                    logger.info(f"達到API限制，等待 {sleep_time:.1f} 秒")
                    time.sleep(sleep_time)
            
            self.requests.put(now)

class OptimizedPPTProcessor:
    """優化的PPT處理器"""
    
    def __init__(self, 
                 gemini_api_key: str,
                 bq_project_id: str,
                 dataset_id: str = "conference_data",
                 table_id: str = "sessions",
                 max_workers: int = 4,
                 max_requests_per_minute: int = 15):
        
        self.gemini_client = genai.Client(api_key=gemini_api_key)
        self.bq_client = OptimizedBigQueryClient(bq_project_id, dataset_id, table_id)
        self.max_workers = max_workers

        # 速率限制器
        self.rate_limiter = RateLimiter(max_requests_per_minute)

        # 緩存BigQuery會議數據
        self.bq_sessions_cache: Dict[str, Tuple[str, str, bool]] = {}
        self.existing_ppt_content: set = set()
        
        logger.info(f"初始化優化PPT處理器: max_workers={max_workers}, rate_limit={max_requests_per_minute}/min")
    
    def _load_bigquery_sessions(self, seminar_name: str) -> None:
        """預載入BigQuery會議數據到緩存 - 使用優化的客戶端"""
        logger.info("載入BigQuery會議數據到緩存...")

        sessions_data = self.bq_client.get_sessions_with_ppt_status(seminar_name)

        for name, (conference_id, _, has_ppt) in sessions_data.items():
            self.bq_sessions_cache[name] = (conference_id, name, has_ppt)
            if has_ppt:
                self.existing_ppt_content.add(conference_id)

        logger.info(f"載入 {len(self.bq_sessions_cache)} 個會議記錄，{len(self.existing_ppt_content)} 個已有PPT內容")
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """計算文本相似度（簡化版本）"""
        # 簡化的相似度計算，可以根據需要優化
        text1_clean = ''.join(c.lower() for c in text1 if c.isalnum())
        text2_clean = ''.join(c.lower() for c in text2 if c.isalnum())
        
        if not text1_clean or not text2_clean:
            return 0.0
        
        # 使用簡單的字符匹配
        matches = sum(1 for c1, c2 in zip(text1_clean, text2_clean) if c1 == c2)
        max_len = max(len(text1_clean), len(text2_clean))
        
        return matches / max_len if max_len > 0 else 0.0
    
    def _find_best_match(self, session_name: str) -> Optional[Tuple[str, str, float]]:
        """在緩存中找到最佳匹配的會議"""
        best_match = None
        best_score = 0.0
        
        for bq_name, (conf_id, _, _) in self.bq_sessions_cache.items():
            score = self._calculate_similarity(session_name, bq_name)
            if score > best_score:
                best_score = score
                best_match = (conf_id, bq_name, score)
        
        # 設定相似度閾值
        if best_match and best_match[2] >= 0.7:
            return best_match
        
        return None
    
    def _extract_ppt_content(self, pdf_path: Path) -> Optional[str]:
        """使用 Gemini API 提取 PPT 內容"""
        try:
            # 應用速率限制
            self.rate_limiter.acquire()
            
            logger.info(f"提取PPT內容: {pdf_path.name}")
            
            # 上傳檔案到 Gemini
            sample_file = self.gemini_client.files.upload(file=pdf_path)
            
            # 提取內容的 prompt
            prompt = f"""
請提取這個 PPT 簡報的完整內容，並按照以下格式整理：

## 簡報標題
{pdf_path.stem}

## 簡報內容
請逐頁提取簡報的文字內容，包括：
- 標題
- 重點內容
- 圖表說明
- 結論

要求：
1. 保持原始內容的邏輯結構
2. 使用 Markdown 格式
3. 保留重要的技術術語和專有名詞
4. 如果有圖表，請描述其主要內容
5. 內容要完整但簡潔

請直接輸出整理後的內容，不需要額外說明。
"""

            # 呼叫 Gemini API
            response = self.gemini_client.models.generate_content(
                model="gemini-2.5-flash-preview-05-20",
                contents=[sample_file, prompt]
            )
            
            return response.text
            
        except Exception as e:
            logger.error(f"提取PPT內容時發生錯誤 ({pdf_path.name}): {e}")
            return None
    
    def _update_bigquery(self, conference_id: str, ppt_content: str) -> bool:
        """更新 BigQuery 中的 ppt_context 欄位 - 使用優化的客戶端"""
        return self.bq_client.update_single_ppt_content(conference_id, ppt_content)
    
    def _process_single_ppt(self, pdf_path: Path) -> PPTProcessingResult:
        """處理單個PPT文件"""
        start_time = time.time()
        session_name = pdf_path.stem
        
        try:
            logger.info(f"處理文件: {session_name}")
            
            # 尋找最佳匹配
            match = self._find_best_match(session_name)
            
            if not match:
                return PPTProcessingResult(
                    file_path=pdf_path,
                    success=False,
                    error=f"未找到匹配的會議: {session_name}",
                    processing_time=time.time() - start_time
                )
            
            conf_id, bq_name, score = match
            logger.info(f"找到匹配: {bq_name} (相似度: {score:.2f})")
            
            # 檢查是否已經有PPT內容
            if conf_id in self.existing_ppt_content:
                logger.info(f"會議已有PPT內容，跳過: {session_name}")
                return PPTProcessingResult(
                    file_path=pdf_path,
                    success=True,
                    conference_id=conf_id,
                    processing_time=time.time() - start_time
                )
            
            # 提取PPT內容
            ppt_content = self._extract_ppt_content(pdf_path)
            if not ppt_content:
                return PPTProcessingResult(
                    file_path=pdf_path,
                    success=False,
                    error="無法提取PPT內容",
                    processing_time=time.time() - start_time
                )
            
            # 更新BigQuery
            if self._update_bigquery(conf_id, ppt_content):
                # 更新緩存
                self.existing_ppt_content.add(conf_id)
                
                return PPTProcessingResult(
                    file_path=pdf_path,
                    success=True,
                    content=ppt_content,
                    conference_id=conf_id,
                    processing_time=time.time() - start_time
                )
            else:
                return PPTProcessingResult(
                    file_path=pdf_path,
                    success=False,
                    error="更新BigQuery失敗",
                    processing_time=time.time() - start_time
                )

    def process_directory(self,
                         input_dir: Path,
                         seminar_name: str,
                         file_pattern: str = "*.pdf") -> ProcessingStats:
        """並行處理目錄中的所有PPT文件"""
        start_time = time.time()

        # 預載入BigQuery數據
        self._load_bigquery_sessions(seminar_name)

        # 查找所有PPT文件
        pdf_files = list(input_dir.glob(file_pattern))
        if not pdf_files:
            logger.warning(f"在目錄 {input_dir} 中沒有找到PPT文件")
            return ProcessingStats()

        logger.info(f"找到 {len(pdf_files)} 個PPT文件，開始並行處理...")

        # 使用線程池並行處理
        results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 提交所有任務
            future_to_file = {
                executor.submit(self._process_single_ppt, pdf_file): pdf_file
                for pdf_file in pdf_files
            }

            # 收集結果
            for future in as_completed(future_to_file):
                pdf_file = future_to_file[future]
                try:
                    result = future.result()
                    results.append(result)

                    if result.success:
                        logger.info(f"✅ 成功處理: {pdf_file.name} ({result.processing_time:.1f}s)")
                    else:
                        logger.error(f"❌ 處理失敗: {pdf_file.name} - {result.error}")

                except Exception as e:
                    logger.error(f"❌ 處理異常: {pdf_file.name} - {e}")
                    results.append(PPTProcessingResult(
                        file_path=pdf_file,
                        success=False,
                        error=str(e)
                    ))

        # 計算統計信息
        total_time = time.time() - start_time
        successful = sum(1 for r in results if r.success)
        failed = len(results) - successful

        stats = ProcessingStats(
            total_files=len(pdf_files),
            successful=successful,
            failed=failed,
            total_time=total_time,
            avg_time_per_file=total_time / len(pdf_files) if pdf_files else 0
        )

        # 輸出統計信息
        logger.info(f"""
處理完成統計:
- 總文件數: {stats.total_files}
- 成功: {stats.successful}
- 失敗: {stats.failed}
- 成功率: {stats.successful/stats.total_files*100:.1f}%
- 總耗時: {stats.total_time:.1f}秒
- 平均每文件: {stats.avg_time_per_file:.1f}秒
        """)

        return stats

    def process_files_batch(self,
                           pdf_files: List[Path],
                           seminar_name: str,
                           batch_size: int = 10) -> ProcessingStats:
        """分批處理PPT文件，適合大量文件"""
        start_time = time.time()

        # 預載入BigQuery數據
        self._load_bigquery_sessions(seminar_name)

        logger.info(f"開始分批處理 {len(pdf_files)} 個文件，批次大小: {batch_size}")

        all_results = []

        # 分批處理
        for i in range(0, len(pdf_files), batch_size):
            batch = pdf_files[i:i + batch_size]
            batch_num = i // batch_size + 1
            total_batches = (len(pdf_files) + batch_size - 1) // batch_size

            logger.info(f"處理批次 {batch_num}/{total_batches} ({len(batch)} 個文件)")

            # 並行處理當前批次
            with ThreadPoolExecutor(max_workers=min(self.max_workers, len(batch))) as executor:
                future_to_file = {
                    executor.submit(self._process_single_ppt, pdf_file): pdf_file
                    for pdf_file in batch
                }

                batch_results = []
                for future in as_completed(future_to_file):
                    pdf_file = future_to_file[future]
                    try:
                        result = future.result()
                        batch_results.append(result)

                        if result.success:
                            logger.info(f"✅ 批次 {batch_num}: {pdf_file.name}")
                        else:
                            logger.error(f"❌ 批次 {batch_num}: {pdf_file.name} - {result.error}")

                    except Exception as e:
                        logger.error(f"❌ 批次 {batch_num} 異常: {pdf_file.name} - {e}")
                        batch_results.append(PPTProcessingResult(
                            file_path=pdf_file,
                            success=False,
                            error=str(e)
                        ))

                all_results.extend(batch_results)

            # 批次間短暫休息
            if i + batch_size < len(pdf_files):
                time.sleep(2)

        # 計算統計信息
        total_time = time.time() - start_time
        successful = sum(1 for r in all_results if r.success)
        failed = len(all_results) - successful

        stats = ProcessingStats(
            total_files=len(pdf_files),
            successful=successful,
            failed=failed,
            total_time=total_time,
            avg_time_per_file=total_time / len(pdf_files) if pdf_files else 0
        )

        logger.info(f"""
分批處理完成統計:
- 總文件數: {stats.total_files}
- 成功: {stats.successful}
- 失敗: {stats.failed}
- 成功率: {stats.successful/stats.total_files*100:.1f}%
- 總耗時: {stats.total_time:.1f}秒
- 平均每文件: {stats.avg_time_per_file:.1f}秒
- 效率提升: 約 {15 * len(pdf_files) / stats.total_time:.1f}x (相比串行處理)
        """)

        return stats
