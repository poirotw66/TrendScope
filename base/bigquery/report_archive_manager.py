"""
報告檔案追蹤管理器
用於管理批量報告生成的ZIP檔案記錄
"""
import uuid
import os
import pathlib
from datetime import datetime
from typing import Dict, Any, List, Optional
import logging

from base.bigquery.client import BigQueryClient
from base.bigquery.schemas.conferences import REPORT_ARCHIVES_SCHEMA

logger = logging.getLogger("NeoTrendHub-api")

class ReportArchiveManager:
    """
    報告檔案追蹤管理器
    負責在BigQuery中記錄和管理報告檔案信息
    """
    
    def __init__(self, bq_client: BigQueryClient):
        """
        初始化報告檔案管理器
        
        Args:
            bq_client (BigQueryClient): BigQuery客戶端
        """
        self.bq_client = bq_client
        self.dataset_id = "conference_data"
        self.table_id = "report_archives"
        
        # 確保表存在
        self._ensure_table_exists()
    
    def _ensure_table_exists(self):
        """確保報告檔案追蹤表存在"""
        try:
            self.bq_client.create_dataset_if_not_exists(self.dataset_id)
            self.bq_client.create_table_if_not_exists(
                self.dataset_id, 
                self.table_id, 
                REPORT_ARCHIVES_SCHEMA
            )
            logger.info(f"報告檔案追蹤表 {self.dataset_id}.{self.table_id} 已準備就緒")
        except Exception as e:
            logger.error(f"創建報告檔案追蹤表失敗: {e}")
            raise
    
    def create_archive_record(
        self,
        task_id: str,
        batch_id: str,
        zip_file_path: str,
        seminars: List[str],
        session_count: int,
        analysis_mode: str = "comprehensive",
        output_template: str = "professional",
        gcs_info: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        
        """
        創建新的檔案追蹤記錄

        Args:
            task_id (str): 任務ID（作為主鍵）
            batch_id (str): 批次ID
            zip_file_path (str): ZIP檔案路徑
            seminars (List[str]): 研討會列表
            session_count (int): 會議數量
            analysis_mode (str): 分析模式
            output_template (str): 輸出模板
            gcs_info (Dict): GCS相關信息
            metadata (Dict): 額外元數據

        Returns:
            str: 任務ID（task_id）
        """
        try:
            zip_path = pathlib.Path(zip_file_path)

            # 構建記錄數據（只包含表結構中定義的欄位）
            record_data = {
                "task_id": task_id,
                "batch_id": batch_id,
                "zip_filename": zip_path.name,
                "seminars": seminars,
                "session_count": session_count,
                "analysis_mode": analysis_mode,
                "output_template": output_template,
                "updated_at": datetime.now().isoformat()
            }

            # 添加GCS信息（如果有）
            if gcs_info and gcs_info.get("success"):
                record_data["gcs_path"] = gcs_info.get("gs_url")
                record_data["gcs_public_url"] = gcs_info.get("public_url")

            # 插入記錄
            self._insert_record(record_data)

            logger.info(f"已創建檔案追蹤記錄: {task_id} for batch {batch_id}")
            return task_id
            
        except Exception as e:
            logger.error(f"創建檔案追蹤記錄失敗: {e}")
            raise
    
    def _insert_record(self, record_data: Dict[str, Any]):
        """插入記錄到BigQuery"""
        try:
            table_ref = f"{self.bq_client.project_id}.{self.dataset_id}.{self.table_id}"
            
            # 使用BigQuery客戶端插入數據
            job = self.bq_client.client.load_table_from_json(
                [record_data], 
                table_ref
            )
            job.result()  # 等待完成
            
            logger.debug(f"檔案記錄已插入BigQuery: {record_data['task_id']}")
            
        except Exception as e:
            logger.error(f"插入檔案記錄到BigQuery失敗: {e}")
            raise
    
    def update_archive_status(self, task_id: str, status: str,
                              gcs_info: Optional[Dict[str, Any]] = None):
        """
        更新檔案狀態

        Args:
            task_id (str): 任務ID
            status (str): 新狀態
            gcs_info (Dict): GCS信息更新
        """
        try:
            update_fields = [
                "updated_at = CURRENT_TIMESTAMP()"
            ]

            if gcs_info and gcs_info.get("success"):
                if gcs_info.get("gs_url"):
                    update_fields.append(f"gcs_path = '{gcs_info['gs_url']}'")
                if gcs_info.get("public_url"):
                    update_fields.append(f"gcs_public_url = '{gcs_info['public_url']}'")

            query = f"""
            UPDATE `{self.bq_client.project_id}.{self.dataset_id}.{self.table_id}`
            SET {', '.join(update_fields)}
            WHERE task_id = '{task_id}'
            """

            job = self.bq_client.client.query(query)
            job.result()

            logger.info(f"已更新檔案記錄: {task_id}")
            
        except Exception as e:
            logger.error(f"更新檔案記錄狀態失敗: {e}")
            raise
    
    def get_archive_by_batch_id(self, batch_id: str) -> Optional[Dict[str, Any]]:
        """
        根據批次ID獲取檔案記錄
        
        Args:
            batch_id (str): 批次ID
            
        Returns:
            Dict: 檔案記錄信息
        """
        try:
            query = f"""
            SELECT *
            FROM `{self.bq_client.project_id}.{self.dataset_id}.{self.table_id}`
            WHERE batch_id = '{batch_id}'
            ORDER BY updated_at DESC
            LIMIT 1
            """
            
            results = self.bq_client.client.query(query)
            for row in results:
                return dict(row)
            
            return None
            
        except Exception as e:
            logger.error(f"獲取檔案記錄失敗: {e}")
            return None
    
    def get_archive_by_task_id(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        根據任務ID獲取檔案記錄
        
        Args:
            task_id (str): 任務ID
            
        Returns:
            Dict: 檔案記錄信息
        """
        try:
            query = f"""
            SELECT *
            FROM `{self.bq_client.project_id}.{self.dataset_id}.{self.table_id}`
            WHERE task_id = '{task_id}'
            ORDER BY updated_at DESC
            LIMIT 1
            """
            
            results = self.bq_client.client.query(query)
            for row in results:
                return dict(row)
            
            return None
            
        except Exception as e:
            logger.error(f"獲取檔案記錄失敗: {e}")
            return None
    
    def list_archives(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        列出檔案記錄

        Args:
            limit (int): 返回記錄數量限制

        Returns:
            List[Dict]: 檔案記錄列表
        """
        try:
            # 由於表結構中沒有 status 欄位，移除狀態過濾
            query = f"""
            SELECT *
            FROM `{self.bq_client.project_id}.{self.dataset_id}.{self.table_id}`
            ORDER BY updated_at DESC
            LIMIT {limit}
            """
            
            results = self.bq_client.client.query(query)
            archives = []
            
            for row in results:
                archive = dict(row)
                # 處理日期時間欄位
                for key, value in archive.items():
                    if hasattr(value, 'isoformat'):
                        archive[key] = value.isoformat()
                archives.append(archive)
            
            return archives
            
        except Exception as e:
            logger.error(f"列出檔案記錄失敗: {e}")
            return []
    
    def delete_archive(self, task_id: str):
        """
        刪除檔案記錄（硬刪除，因為表結構中沒有status欄位）

        Args:
            task_id (str): 任務ID
        """
        try:
            query = f"""
            DELETE FROM `{self.bq_client.project_id}.{self.dataset_id}.{self.table_id}`
            WHERE task_id = '{task_id}'
            """

            job = self.bq_client.client.query(query)
            job.result()

            logger.info(f"已刪除檔案記錄: {task_id}")

        except Exception as e:
            logger.error(f"刪除檔案記錄失敗: {e}")
            raise
