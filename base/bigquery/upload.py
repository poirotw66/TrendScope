"""
BigQuery 上傳模組
提供將爬蟲資料上傳到 BigQuery 的功能
"""
from datetime import datetime
import uuid
from google.cloud import bigquery

from base.bigquery.client import BigQueryClient
from base.bigquery.schemas.conferences import CONFERENCE_SCHEMA

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
        
    def _check_existing_sessions(self, sessions):
        """
        檢查哪些會議已經存在於 BigQuery 中（基於 name 和 seminar 組合）

        Args:
            sessions (list): 會議資料列表

        Returns:
            set: 已存在的 (name, seminar) 組合集合
        """
        if not sessions:
            return set()

        # 構建查詢條件
        conditions = []
        for session in sessions:
            name = session.get("name", session.get("會議名稱", ""))
            seminar = session.get("seminar", "")
            if name and seminar:
                conditions.append(f"(name = '{name.replace(chr(39), chr(39)+chr(39))}' AND seminar = '{seminar.replace(chr(39), chr(39)+chr(39))}')")

        if not conditions:
            return set()

        # 查詢已存在的記錄
        query = f"""
        SELECT name, seminar
        FROM `{self.bq_client.project_id}.{self.dataset_id}.{self.table_id}`
        WHERE {' OR '.join(conditions)}
        """

        try:
            results = self.bq_client.client.query(query)
            existing = set()
            for row in results:
                existing.add((row.name, row.seminar))
            return existing
        except Exception as e:
            print(f"檢查現有記錄時發生錯誤: {str(e)}")
            return set()

    def upload_sessions(self, sessions, source):
        """
        上傳會議資料到 BigQuery，避免重複上傳相同的 name 和 seminar 組合

        Args:
            sessions (list): 會議資料列表，每個元素為一個字典
            source (str): 資料來源，例如 "AWS London Summit"

        Returns:
            bool: 上傳是否成功
        """
        if not sessions:
            print("沒有資料可上傳")
            return False
        
        # 檢查已存在的記錄
        existing_sessions = self._check_existing_sessions(sessions)
        print(f"發現 {len(existing_sessions)} 個已存在的會議記錄")

        # 轉換資料格式，過濾掉重複的記錄
        bq_data = []
        skipped_count = 0
        current_time = datetime.now().isoformat()

        for session in sessions:
            # 檢查是否為重複記錄
            session_name = session.get("name", session.get("會議名稱", ""))
            session_seminar = session.get("seminar", source)

            if (session_name, session_seminar) in existing_sessions:
                print(f"跳過重複記錄: {session_name} (seminar: {session_seminar})")
                skipped_count += 1
                continue

            # 使用提供的ID或生成新ID
            session_id = session.get("conference_id", str(uuid.uuid4()))

            # 轉換為 BigQuery 格式
            bq_session = {
                "conference_id": session_id,
                "seminar": session_seminar,
                "name": session_name,
                "description": session.get("description", session.get("描述", "")),
                "url": session.get("url", session.get("會議連結", "")),
                "pdf_url": session.get("pdf_url", session.get("PDF 連結", "")),
                "tags": session.get("tags", session.get("標籤", "").split(", ") if session.get("標籤") else []),
                "created_at": current_time,
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

        # 檢查是否有新數據需要上傳
        if not bq_data:
            print(f"所有 {len(sessions)} 條記錄都已存在，跳過上傳")
            return True

        print(f"準備上傳 {len(bq_data)} 條新記錄，跳過 {skipped_count} 條重複記錄")

        try:
            # 創建臨時表
            temp_table_id = f"temp_{uuid.uuid4().hex}"
            temp_table_ref = f"{self.bq_client.project_id}.{self.dataset_id}.{temp_table_id}"
            
            # 上傳數據到臨時表
            job_config = bigquery.LoadJobConfig(
                schema=CONFERENCE_SCHEMA,
                write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
            )
            
            job = self.bq_client.client.load_table_from_json(
                bq_data, 
                temp_table_ref,
                job_config=job_config
            )
            job.result()  # 等待完成
            
            # 使用MERGE語句合併數據，基於 name 和 seminar 的組合來避免重複
            merge_query = f"""
            MERGE `{self.bq_client.project_id}.{self.dataset_id}.{self.table_id}` T
            USING `{temp_table_ref}` S
            ON T.name = S.name AND T.seminar = S.seminar
            WHEN MATCHED THEN
              UPDATE SET
                description = COALESCE(S.description, T.description),
                url = COALESCE(S.url, T.url),
                pdf_url = COALESCE(S.pdf_url, T.pdf_url),
                tags = COALESCE(S.tags, T.tags),
                conference_id = COALESCE(S.conference_id, T.conference_id)
            WHEN NOT MATCHED THEN
              INSERT (conference_id, seminar, name, description, url, pdf_url, tags, created_at)
              VALUES (
                S.conference_id,
                S.seminar,
                S.name,
                S.description,
                S.url,
                S.pdf_url,
                S.tags,
                S.created_at
              )
            """
            
            merge_job = self.bq_client.client.query(merge_query)
            merge_job.result()
            
            # 刪除臨時表
            self.bq_client.client.delete_table(temp_table_ref)

            print(f"成功上傳 {len(bq_data)} 條新會議資料到 BigQuery，跳過 {skipped_count} 條重複記錄")
            return True
        
        except Exception as e:
            print(f"上傳到 BigQuery 失敗: {str(e)}")
            return False
