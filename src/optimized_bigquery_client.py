"""
優化的 BigQuery 客戶端
實現連接池、批量操作和查詢優化
"""

import logging
import time
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

from google.cloud import bigquery
from google.cloud.bigquery import LoadJobConfig, WriteDisposition, QueryJobConfig

logger = logging.getLogger(__name__)

@dataclass
class BatchUpdateResult:
    """批量更新結果"""
    total_updates: int
    successful_updates: int
    failed_updates: int
    errors: List[str]
    processing_time: float

class OptimizedBigQueryClient:
    """優化的BigQuery客戶端"""
    
    def __init__(self, project_id: str, dataset_id: str = "conference_data", table_id: str = "sessions"):
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id
        self.client = bigquery.Client(project=project_id)
        self.table_ref = self.client.dataset(dataset_id).table(table_id)
        
        # 連接池和緩存
        self._connection_pool = []
        self._cache = {}
        self._cache_lock = threading.Lock()
        
        logger.info(f"初始化優化BigQuery客戶端: {project_id}.{dataset_id}.{table_id}")
    
    def get_sessions_with_ppt_status(self, seminar_name: str) -> Dict[str, Tuple[str, str, bool]]:
        """獲取會議列表及PPT狀態 - 單次查詢優化"""
        cache_key = f"sessions_{seminar_name}"
        
        with self._cache_lock:
            if cache_key in self._cache:
                logger.info("使用緩存的會議數據")
                return self._cache[cache_key]
        
        logger.info(f"查詢會議數據: {seminar_name}")
        
        query = f"""
        SELECT 
            conference_id, 
            name, 
            ppt_context IS NOT NULL AND LENGTH(TRIM(ppt_context)) > 0 as has_ppt,
            COALESCE(LENGTH(ppt_context), 0) as ppt_length
        FROM `{self.project_id}.{self.dataset_id}.{self.table_id}` 
        WHERE seminar = @seminar_name
        ORDER BY name
        """
        
        job_config = QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("seminar_name", "STRING", seminar_name),
            ],
            use_query_cache=True,  # 啟用查詢緩存
            use_legacy_sql=False
        )
        
        start_time = time.time()
        results = self.client.query(query, job_config=job_config)
        
        sessions_data = {}
        for row in results:
            sessions_data[row['name']] = (
                row['conference_id'], 
                row['name'], 
                row['has_ppt']
            )
        
        query_time = time.time() - start_time
        logger.info(f"查詢完成: {len(sessions_data)} 個會議，耗時 {query_time:.2f}秒")
        
        # 緩存結果
        with self._cache_lock:
            self._cache[cache_key] = sessions_data
        
        return sessions_data
    
    def batch_update_ppt_content(self, updates: List[Tuple[str, str]], batch_size: int = 50) -> BatchUpdateResult:
        """批量更新PPT內容 - 使用事務和批量操作"""
        start_time = time.time()
        total_updates = len(updates)
        successful_updates = 0
        failed_updates = 0
        errors = []
        
        logger.info(f"開始批量更新 {total_updates} 個PPT內容，批次大小: {batch_size}")
        
        # 分批處理
        for i in range(0, total_updates, batch_size):
            batch = updates[i:i + batch_size]
            batch_num = i // batch_size + 1
            total_batches = (total_updates + batch_size - 1) // batch_size
            
            logger.info(f"處理批次 {batch_num}/{total_batches} ({len(batch)} 個更新)")
            
            try:
                # 構建批量更新查詢
                update_cases = []
                conference_ids = []
                
                for j, (conference_id, ppt_content) in enumerate(batch):
                    param_name = f"content_{i}_{j}"
                    update_cases.append(f"WHEN @conf_id_{i}_{j} THEN @{param_name}")
                    conference_ids.append(conference_id)
                
                # 批量更新SQL
                update_query = f"""
                UPDATE `{self.project_id}.{self.dataset_id}.{self.table_id}` 
                SET ppt_context = CASE conference_id
                    {' '.join(update_cases)}
                    ELSE ppt_context
                END
                WHERE conference_id IN ({','.join(['@conf_id_' + str(i) + '_' + str(j) for j in range(len(batch))])})
                """
                
                # 準備參數
                query_parameters = []
                for j, (conference_id, ppt_content) in enumerate(batch):
                    query_parameters.extend([
                        bigquery.ScalarQueryParameter(f"conf_id_{i}_{j}", "STRING", conference_id),
                        bigquery.ScalarQueryParameter(f"content_{i}_{j}", "STRING", ppt_content)
                    ])
                
                job_config = QueryJobConfig(query_parameters=query_parameters)
                
                # 執行批量更新
                job = self.client.query(update_query, job_config=job_config)
                job.result()
                
                successful_updates += len(batch)
                logger.info(f"批次 {batch_num} 更新成功: {len(batch)} 個記錄")
                
            except Exception as e:
                error_msg = f"批次 {batch_num} 更新失敗: {str(e)}"
                logger.error(error_msg)
                errors.append(error_msg)
                failed_updates += len(batch)
                
                # 嘗試單個更新作為備用方案
                logger.info(f"嘗試單個更新批次 {batch_num}")
                for conference_id, ppt_content in batch:
                    try:
                        if self.update_single_ppt_content(conference_id, ppt_content):
                            successful_updates += 1
                            failed_updates -= 1
                    except Exception as single_error:
                        logger.error(f"單個更新失敗 {conference_id}: {single_error}")
        
        processing_time = time.time() - start_time
        
        result = BatchUpdateResult(
            total_updates=total_updates,
            successful_updates=successful_updates,
            failed_updates=failed_updates,
            errors=errors,
            processing_time=processing_time
        )
        
        logger.info(f"""
批量更新完成:
- 總數: {result.total_updates}
- 成功: {result.successful_updates}
- 失敗: {result.failed_updates}
- 成功率: {result.successful_updates/result.total_updates*100:.1f}%
- 耗時: {result.processing_time:.2f}秒
        """)
        
        return result
    
    def update_single_ppt_content(self, conference_id: str, ppt_content: str) -> bool:
        """更新單個PPT內容 - 優化版本"""
        try:
            update_query = f"""
            UPDATE `{self.project_id}.{self.dataset_id}.{self.table_id}` 
            SET ppt_context = @ppt_content,
                updated_at = CURRENT_TIMESTAMP()
            WHERE conference_id = @conference_id
            """
            
            job_config = QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("ppt_content", "STRING", ppt_content),
                    bigquery.ScalarQueryParameter("conference_id", "STRING", conference_id),
                ],
                use_query_cache=False,  # 更新操作不使用緩存
                dry_run=False
            )
            
            job = self.client.query(update_query, job_config=job_config)
            job.result()
            
            return True
            
        except Exception as e:
            logger.error(f"更新單個PPT內容失敗 {conference_id}: {e}")
            return False
    
    def check_ppt_exists_batch(self, conference_ids: List[str]) -> Dict[str, bool]:
        """批量檢查PPT內容是否存在"""
        if not conference_ids:
            return {}
        
        logger.info(f"批量檢查 {len(conference_ids)} 個會議的PPT狀態")
        
        # 構建IN查詢
        placeholders = [f"@conf_id_{i}" for i in range(len(conference_ids))]
        query = f"""
        SELECT 
            conference_id,
            ppt_context IS NOT NULL AND LENGTH(TRIM(ppt_context)) > 0 as has_ppt
        FROM `{self.project_id}.{self.dataset_id}.{self.table_id}` 
        WHERE conference_id IN ({','.join(placeholders)})
        """
        
        query_parameters = [
            bigquery.ScalarQueryParameter(f"conf_id_{i}", "STRING", conf_id)
            for i, conf_id in enumerate(conference_ids)
        ]
        
        job_config = QueryJobConfig(
            query_parameters=query_parameters,
            use_query_cache=True
        )
        
        results = self.client.query(query, job_config=job_config)
        
        ppt_status = {}
        for row in results:
            ppt_status[row['conference_id']] = row['has_ppt']
        
        # 對於沒有找到的會議ID，設為False
        for conf_id in conference_ids:
            if conf_id not in ppt_status:
                ppt_status[conf_id] = False
        
        return ppt_status
    
    def get_table_stats(self) -> Dict[str, Any]:
        """獲取表格統計信息"""
        query = f"""
        SELECT 
            COUNT(*) as total_sessions,
            COUNT(ppt_context) as sessions_with_ppt,
            AVG(LENGTH(ppt_context)) as avg_ppt_length,
            MAX(LENGTH(ppt_context)) as max_ppt_length
        FROM `{self.project_id}.{self.dataset_id}.{self.table_id}`
        WHERE ppt_context IS NOT NULL
        """
        
        results = self.client.query(query)
        for row in results:
            return {
                'total_sessions': row['total_sessions'],
                'sessions_with_ppt': row['sessions_with_ppt'],
                'avg_ppt_length': row['avg_ppt_length'],
                'max_ppt_length': row['max_ppt_length']
            }
        
        return {}
    
    def clear_cache(self):
        """清除緩存"""
        with self._cache_lock:
            self._cache.clear()
        logger.info("BigQuery緩存已清除")
