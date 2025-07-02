"""
BigQuery 上傳模組
提供將爬蟲資料上傳到 BigQuery 的功能
"""
from datetime import datetime
import uuid
from google.cloud import bigquery

from bigquery.client import BigQueryClient
from bigquery.schemas.conferences import CONFERENCE_SCHEMA

class ConferenceUploader:
    """
    會議資料上傳器
    用於將爬蟲獲取的會議資料上傳到 BigQuery
    """
    
    def __init__(self, credentials_path=None, project_id=None):
        """
        初始化上傳器
        
        Args:
            credentials_path (str, optional): Google Cloud 服務帳戶憑證路徑
            project_id (str, optional): Google Cloud 項目 ID
        """
        self.bq_client = BigQueryClient(credentials_path, project_id)
        self.dataset_id = "conference_data"
        self.table_id = "sessions"
        
        # 確保資料集和資料表存在
        self.bq_client.create_dataset_if_not_exists(self.dataset_id)
        self.bq_client.create_table_if_not_exists(self.dataset_id, self.table_id, CONFERENCE_SCHEMA)
        
    def upload_sessions(self, sessions, source):
        """
        上傳會議資料到 BigQuery
        
        Args:
            sessions (list): 會議資料列表，每個元素為一個字典
            source (str): 資料來源，例如 "AWS London Summit"
            
        Returns:
            bool: 上傳是否成功
        """
        if not sessions:
            print("沒有資料可上傳")
            return False
            
        # 轉換資料格式
        bq_data = []
        current_time = datetime.now().isoformat()
        
        for session in sessions:
            # 創建唯一 ID
            session_id = str(uuid.uuid4())
            
            # 轉換為 BigQuery 格式
            bq_session = {
                "conference_id": session.get("conference_id", session_id),  # Use provided ID or generate a new one
                "seminar": session.get("seminar", session_id),
                "name": session.get("name", session.get("會議名稱", "")),
                "description": session.get("description", session.get("描述", "")),
                "url": session.get("url", session.get("會議連結", "")),
                "pdf_url": session.get("pdf_url", session.get("PDF 連結", "")),
                "tags": session.get("tags", session.get("標籤", "").split(", ") if session.get("標籤") else []),
                "created_at": current_time,  # Always use current timestamp for created_at to ensure it's non-null
            }
            
            # 處理講者資訊（如果有）
            if "講者" in session and session["講者"]:
                speakers_list = []
                for speaker in session["講者"].split(", "):
                    speakers_list.append({
                        "name": speaker,
                        "title": "",
                        "company": ""
                    })
                bq_session["speakers"] = speakers_list
                
            bq_data.append(bq_session)
            
        try:
            # 上傳到 BigQuery
            self.bq_client.upload_data_to_table(
                self.dataset_id, 
                self.table_id, 
                bq_data
            )
            print(f"成功上傳 {len(bq_data)} 條會議資料到 BigQuery")
            return True
        except Exception as e:
            print(f"上傳到 BigQuery 失敗: {str(e)}")
            return False
